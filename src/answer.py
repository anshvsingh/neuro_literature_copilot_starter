"""Extractive question answering over retrieved evidence passages.

Given a question and the passages returned by ``research.prepare_evidence``,
this module picks the sentence span in each passage that best answers the
question, ranks those spans, and returns:

* a main answer (the best-scoring span),
* alternative answers (other well-scoring spans, preferring other papers),
* for every answer, the exact source chunk with the character offsets of the
  quoted span, so the UI can show and highlight where the answer came from.

Answers are quoted verbatim from the papers; nothing is generated. Spans that
say nearly the same thing are merged, and the extra sources are listed as
corroborating evidence for the answer they repeat.
"""

import re

import numpy as np

from src.retrieve import get_embedding_model

# Sentence boundary: end punctuation followed by whitespace and a likely sentence start.
_SENTENCE_BOUNDARY = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[“\"])")

_STOPWORDS = {
    "about", "above", "across", "after", "again", "against", "also", "among", "and",
    "any", "are", "based", "been", "being", "between", "both", "but", "can", "could",
    "did", "does", "doing", "during", "each", "for", "from", "further", "had", "has",
    "have", "how", "into", "its", "itself", "more", "most", "other", "over", "reported",
    "same", "should", "some", "such", "than", "that", "the", "their", "them", "then",
    "there", "these", "they", "this", "those", "through", "under", "until", "used",
    "using", "very", "was", "were", "what", "when", "where", "which", "while", "who",
    "whom", "why", "will", "with", "within", "without", "would", "your",
}

MAX_SPAN_CHARS = 480
NEAR_DUPLICATE_SIMILARITY = 0.86
SIMILAR_TO_MAIN_SIMILARITY = 0.70
TRUNCATED_PENALTY = 0.05
MIN_ALTERNATIVE_SCORE = 0.40


def split_sentences(text):
    """Split text into sentences, returning (start, end) character offsets."""
    spans = []
    start = 0
    for match in _SENTENCE_BOUNDARY.finditer(text):
        end = match.start()
        if text[start:end].strip():
            spans.append((start, end))
        start = match.end()
    if text[start:].strip():
        spans.append((start, len(text.rstrip())))
    return spans


def is_answerable_sentence(sentence):
    """Reject fragments that cannot stand on their own as an answer."""
    s = sentence.strip()
    if len(s) < 40:
        return False
    words = re.findall(r"[A-Za-z]{2,}", s)
    if len(words) < 8:
        return False
    letters = sum(ch.isalpha() for ch in s)
    if letters / max(len(s), 1) < 0.6:
        return False
    # Bibliography-like lines: many bracketed refs, years, or "et al." with little prose.
    if len(re.findall(r"\[\d+(?:[,–-]\s*\d+)*\]", s)) >= 4:
        return False
    if len(re.findall(r"\b(19|20)\d{2}\b", s)) >= 3 and "et al" in s:
        return False
    if re.search(r"\bdoi\b|https?://|©|all rights reserved", s, re.I):
        return False
    # Figure/table captions echo topic words but rarely state a finding.
    if re.match(r"\s*(fig\.?|figure|table)\s*[0-9IVX]+", s, re.I):
        return False
    # Title or author lines are mostly capitalised words.
    long_words = [w for w in words if len(w) > 3]
    if long_words and sum(w[0].isupper() for w in long_words) / len(long_words) > 0.6:
        return False
    # Funding, disclosure, and acknowledgement statements are never answers.
    if re.search(
        r"honorari|conflicts? of interest|competing interests?|grant (?:no|number)|"
        r"funded by|acknowledg|associate editor|advisory board|corresponding author",
        s, re.I,
    ):
        return False
    return True


def _keywords(text):
    """Content-word stems used for lexical overlap scoring."""
    tokens = re.findall(r"[a-z][a-z0-9-]{2,}", text.lower())
    return {t[:6] for t in tokens if t not in _STOPWORDS}


def _lexical_overlap(question_terms, sentence):
    if not question_terms:
        return 0.0
    return len(question_terms & _keywords(sentence)) / len(question_terms)


def _confidence_label(score):
    if score >= 0.55:
        return "high"
    if score >= 0.42:
        return "medium"
    return "low"


def _best_span(passage, sentence_spans, scores):
    """Return (start, end, score, sentence_indices) of the best span in a passage.

    The span is the top sentence, extended by one neighbour when that neighbour
    is nearly as relevant, so short sentences keep their context.
    """
    best = int(np.argmax(scores))
    chosen = [best]
    best_score = float(scores[best])

    neighbours = [i for i in (best - 1, best + 1) if 0 <= i < len(sentence_spans)]
    neighbours.sort(key=lambda i: scores[i], reverse=True)
    for i in neighbours:
        if scores[i] < best_score - 0.08:
            continue
        lo = min(chosen + [i])
        hi = max(chosen + [i])
        if sentence_spans[hi][1] - sentence_spans[lo][0] <= MAX_SPAN_CHARS:
            chosen.append(i)
            break

    chosen.sort()
    start = sentence_spans[chosen[0]][0]
    end = sentence_spans[chosen[-1]][1]
    span_score = float(np.mean([scores[i] for i in chosen]))
    # Reward the best sentence more than the averaged span so extensions never hurt ranking.
    span_score = max(span_score, best_score - 0.02)
    return start, end, span_score, chosen


def _source_fields(item):
    pid = item.get("paper_id", "UNKNOWN")
    page = item.get("page", 1)
    return {
        "citation": f"{pid}, p. {page}",
        "paper_id": pid,
        "page": page,
        "chunk_id": item.get("chunk_id", ""),
        "condition": item.get("condition", ""),
        "source_file": item.get("source_file", ""),
    }


def build_answers(question, evidence, max_alternatives=5):
    """Pick a main answer and alternative answers from retrieved passages.

    Returns a dict with ``answer`` (or None), ``alternatives``, and counts.
    Every answer carries its exact passage and ``highlight`` offsets.
    """
    candidates = []
    model = get_embedding_model()
    question_terms = _keywords(question)
    q_emb = model.encode([question], normalize_embeddings=True)[0]

    # Collect answerable sentences from every passage and embed them in one batch.
    per_passage = []
    all_sentences = []
    for item in evidence:
        passage = item.get("passage", "") or ""
        spans = [
            (s, e) for (s, e) in split_sentences(passage)
            if is_answerable_sentence(passage[s:e])
            # Chunks often begin mid-sentence; a lowercase opening is a fragment.
            and not (s == 0 and passage[:1].islower())
        ]
        if not spans:
            continue
        per_passage.append((item, passage, spans, len(all_sentences)))
        all_sentences.extend(passage[s:e] for s, e in spans)

    if not all_sentences:
        return {"answer": None, "alternatives": [], "passages_considered": len(evidence)}

    sent_embs = model.encode(all_sentences, normalize_embeddings=True, show_progress_bar=False)
    semantic = sent_embs @ q_emb

    for item, passage, spans, offset in per_passage:
        sims = semantic[offset:offset + len(spans)]
        lexical = np.array([_lexical_overlap(question_terms, passage[s:e]) for s, e in spans])
        scores = 0.85 * sims + 0.15 * lexical
        # Chunks are cut at fixed sizes, so the last sentence may be unfinished.
        truncated = np.array([not passage[s:e].rstrip().endswith((".", "!", "?", ")", "]")) for s, e in spans])
        scores = scores - TRUNCATED_PENALTY * truncated

        start, end, score, idxs = _best_span(passage, spans, scores)
        emb = sent_embs[[offset + i for i in idxs]].mean(axis=0)
        emb = emb / (np.linalg.norm(emb) or 1.0)

        candidates.append({
            **_source_fields(item),
            "text": passage[start:end].strip(),
            "score": round(score, 4),
            "confidence": _confidence_label(score),
            "passage": passage,
            "highlight": {"start": start, "end": end},
            "retrieval_rank": item.get("rank"),
            "supporting_sources": [],
            "_emb": emb,
        })

    candidates.sort(key=lambda c: c["score"], reverse=True)

    # Merge near-duplicate spans into the first answer that says the same thing.
    distinct = []
    for cand in candidates:
        duplicate_of = None
        for kept in distinct:
            if float(cand["_emb"] @ kept["_emb"]) >= NEAR_DUPLICATE_SIMILARITY:
                duplicate_of = kept
                break
        if duplicate_of is not None:
            duplicate_of["supporting_sources"].append({
                **_source_fields(cand),
                "text": cand["text"],
                "highlight": cand["highlight"],
            })
        else:
            distinct.append(cand)

    main = distinct[0]
    rest = [c for c in distinct[1:] if c["score"] >= MIN_ALTERNATIVE_SCORE]

    # Prefer alternatives from papers not already shown, then fill with the rest.
    seen_papers = {main["paper_id"]}
    alternatives = []
    for cand in rest:
        if cand["paper_id"] not in seen_papers:
            alternatives.append(cand)
            seen_papers.add(cand["paper_id"])
    for cand in rest:
        if cand not in alternatives:
            alternatives.append(cand)
    alternatives = alternatives[:max_alternatives]
    alternatives.sort(key=lambda c: c["score"], reverse=True)

    for cand in alternatives:
        sim = float(cand["_emb"] @ main["_emb"])
        cand["similarity_to_main"] = round(sim, 4)
        cand["relation"] = "similar" if sim >= SIMILAR_TO_MAIN_SIMILARITY else "different"

    for cand in [main] + alternatives:
        cand.pop("_emb", None)

    return {
        "answer": main,
        "alternatives": alternatives,
        "passages_considered": len(evidence),
        "method": "extractive",
    }
