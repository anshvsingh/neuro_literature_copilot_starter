
import argparse
import json
import re
from datetime import datetime
from pathlib import Path

from src.retrieve import search


OUTPUT_DIR = Path("outputs")

VALID_CONDITIONS = [
    "alzheimers",
    "epilepsy",
    "parkinsons",
    "schizophrenia",
]




def assess_passage(passage):
    """Flag likely bibliography and publication-metadata passages."""
    text = passage.strip()

    if not text:
        return {
            "review_warnings": ["Passage is empty"],
            "is_reference_heavy": True,
            "needs_manual_support_check": True,
        }

    # Remove common PDF extraction control characters.
    clean = re.sub(r"[\x00-\x1f]+", " ", text)
    lower = clean.lower()
    warnings = []

    # Detect reference-section headings.
    heading = re.search(
        r"\b(references|bibliography|reference list)\b",
        clean,
        re.IGNORECASE,
    )

    # Count common citation and publication signals.
    years = re.findall(
        r"\b(?:19|20)\d{2}[a-z]?\b",
        clean,
        re.IGNORECASE,
    )

    numbered = re.findall(
        r"(?<!\w)(?:\[\d{1,3}\]|\d{1,3}[.)])\s+[A-Z]",
        clean,
    )

    # Author formats such as "Smith, J." or "Smith, J. R."
    authors = re.findall(
        r"\b[A-Z][A-Za-z'’.-]+,\s*"
        r"(?:[A-Z]\.?\s*){1,3}",
        clean,
    )

    dois = len(re.findall(
        r"\bdoi\s*:\s*|\bdoi\.org/",
        lower,
    ))

    urls = len(re.findall(
        r"https?://|www\.",
        lower,
    ))

    # Publication terms, including common abbreviated journal names.
    journal_terms = len(re.findall(
        r"\b(journal|proceedings|vol\.?|volume|pp\.?|pages|"
        r"conference|crossref|pubmed|ieee|springer|elsevier|"
        r"lancet|neurol\.?|comput\.?|med\.?|plos|frontiers|"
        r"neuroimage|radiat\.?|oncol\.?|mov\.?\s+disord)\b",
        lower,
    ))

    # Typical bibliography page ranges, e.g. 235-245 or 545–563.
    page_ranges = len(re.findall(
        r"\b\d{1,4}\s*[-–]\s*\d{1,4}\b",
        clean,
    ))

    # Publication metadata often dominates the first page of a paper.
    metadata_terms = len(re.findall(
        r"\b(academic editor|received|accepted|published|"
        r"copyright|open access|correspondence|citation:|"
        r"article|license|affiliations)\b",
        lower,
    ))

    # Rule 1: a reference heading plus multiple bibliography signals.
    heading_bibliography = bool(
        heading
        and (
            len(numbered) >= 2
            or (len(years) >= 3 and len(authors) >= 2)
            or (journal_terms >= 3 and len(years) >= 2)
        )
    )

    # Rule 2: numbered references even when the heading is absent.
    numbered_bibliography = bool(
        len(numbered) >= 2
        and (
            len(years) >= 2
            or journal_terms >= 2
            or dois + urls >= 1
        )
        and (
            len(authors) >= 2
            or journal_terms >= 3
            or dois + urls >= 1
        )
    )

    # Rule 3: author-year bibliography entries without a heading.
    # Requires several author names, years, and publication clues.
    author_year_bibliography = bool(
        len(authors) >= 3
        and len(years) >= 3
        and (
            page_ranges >= 2
            or journal_terms >= 2
            or dois + urls >= 1
        )
    )

    # Rule 4: dense clusters of citation and journal information.
    dense_bibliography = bool(
        len(years) >= 5
        and len(authors) >= 4
        and (
            journal_terms >= 3
            or page_ranges >= 2
            or dois + urls >= 1
        )
    )

    # Rule 5: publication metadata dominating a short passage.
    metadata_heavy = bool(
        metadata_terms >= 4
        and len(clean) < 1800
        and (
            dois >= 1
            or urls >= 1
            or len(years) >= 2
        )
    )

    reference_heavy = (
        heading_bibliography
        or numbered_bibliography
        or author_year_bibliography
        or dense_bibliography
        or metadata_heavy
    )

    if heading:
        warnings.append("Contains a reference-section heading")

    if author_year_bibliography:
        warnings.append(
            "Contains multiple author-year bibliography patterns"
        )

    if metadata_heavy:
        warnings.append(
            "Contains substantial publication metadata"
        )

    if reference_heavy:
        warnings.append(
            "Likely reference-list or metadata-heavy passage"
        )

    if len(clean) < 150:
        warnings.append(
            "Short passage; may provide insufficient context"
        )

    return {
        "review_warnings": warnings,
        "is_reference_heavy": reference_heavy,
        "needs_manual_support_check": True,
    }



def prepare_evidence(question, top_k=5, condition=None):
    """
    Retrieve extra candidates, assess their quality, and return
    the best available passages that are not flagged as references.
    """
    candidate_count = min(max(top_k * 4, top_k), 40)

    results = search(
        query=question,
        top_k=candidate_count,
        condition=condition,
    )

    if not results:
        return []

    assessed_results = []

    for result in results:
        item = dict(result)

        assessment = assess_passage(
            item.get("passage", "")
        )

        item["review_warnings"] = assessment["review_warnings"]
        item["is_reference_heavy"] = assessment["is_reference_heavy"]
        item["needs_manual_support_check"] = assessment[
            "needs_manual_support_check"
        ]

        assessed_results.append(item)

    # Never fill the report with passages flagged as reference-heavy.
    clean_results = [
        item
        for item in assessed_results
        if not item["is_reference_heavy"]
    ]

    # Preserve the original retrieval order among clean results.
    selected_results = clean_results[:top_k]

    for rank, item in enumerate(selected_results, start=1):
        item["rank"] = rank

    return selected_results


def _source_label(item):
    """Return a compact paper/page citation for an evidence passage."""
    paper = item.get("paper_id", "Unknown paper")
    page = item.get("page", "?")
    return f"{paper}, p. {page}"


def synthesize_evidence(question, evidence):
    """Create a transparent, rule-based synthesis from retrieved passages.

    This is a lightweight baseline, not a language-model-generated review.
    Themes and gaps are surfaced only when relevant terms occur in the
    selected passages. Human verification is still required.
    """
    modality_patterns = {
        "MRI (including structural and T1/T2-weighted MRI)":
            r"\bMRI\b|magnetic resonance|T1[- ]weighted|T2[- ]weighted",
        "SPECT": r"\bSPECT\b",
        "DaTscan": r"\bDaTscan\b|dopamine transporter scan",
        "diffusion tensor imaging (DTI)": r"diffusion tensor imaging|\bDTI\b",
        "neuromelanin-sensitive imaging": r"neuromelanin",
        "CT": r"\bCT scans?\b|computed tomography",
        "multimodal imaging": r"multimodal|multiple imaging techniques|combination of multiple imaging",
    }
    model_patterns = {
        "Convolutional neural networks (CNNs)": r"\bCNNs?\b|convolutional neural network",
        "3D CNNs": r"3[- ]dimensional CNN|3D CNN|three[- ]dimensional CNN",
        "AlexNet / transfer learning": r"AlexNet|transfer learning",
        "DenseNet": r"DenseNet",
        "deep learning (general)": r"deep learning",
        "computer-aided diagnosis (CAD)": r"computer[- ]aided diagnosis|\bCAD\b",
        "graph convolutional networks (GCNs)": r"\bGCNs?\b|graph convolutional",
    }

    def collect_terms(patterns):
        found = {}
        for label, pattern in patterns.items():
            matching = [item for item in evidence
                        if re.search(pattern, item.get("passage", ""), re.I)]
            if matching:
                found[label] = matching
        return found

    modalities = collect_terms(modality_patterns)
    models = collect_terms(model_patterns)

    # Group the retrieved passages by paper, preserving source/page traceability.
    papers = {}
    for item in evidence:
        paper_id = item.get("paper_id", "Unknown paper")
        papers.setdefault(paper_id, []).append(item)

    # Surface candidate limitations only when explicit cues appear in evidence.
    gap_cues = {
        "Validation and generalizability":
            r"generaliz|external validation|larger[- ]scale validation|independent validation|cross[- ]validation|data splitting",
        "Potential data leakage or evaluation concerns":
            r"data leakage|overestimation|train(?:ing)?[- ]test split|cross[- ]validation|data splitting",
        "Clinical translation and routine-use limitations":
            r"clinical translation|routine use|clinical practice|translation into hospitals|not specifically recommended",
        "Need to evaluate multimodal approaches":
            r"multimodal|multiple imaging techniques|combination of multiple imaging",
        "Modality coverage may be incomplete":
            r"not yet extended|future work|have not yet|MRI scans or CT scans",
    }
    candidate_gaps = []
    for label, pattern in gap_cues.items():
        matches = [item for item in evidence
                   if re.search(pattern, item.get("passage", ""), re.I)]
        if matches:
            candidate_gaps.append({
                "topic": label,
                "evidence": matches,
                "note": (
                    "Candidate issue mentioned in the retrieved passages; "
                    "check the full papers before treating it as a research gap."
                ),
            })

    return {
        "modalities": modalities,
        "models": models,
        "papers": papers,
        "candidate_gaps": candidate_gaps,
    }


def _format_term_section(lines, heading, groups):
    lines.extend([f"### {heading}", ""])
    if not groups:
        lines.extend(["No clear matches were identified in the selected passages.", ""])
        return
    for label, items in groups.items():
        sources = ", ".join(dict.fromkeys(_source_label(item) for item in items))
        lines.append(f"- **{label}:** mentioned in {sources}.")
    lines.append("")


def make_report(question, evidence, condition=None):
    """Create a Markdown report with evidence-linked rule-based synthesis."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    synthesis = synthesize_evidence(question, evidence)

    lines = [
        "# Neuro Literature Research Report", "",
        f"**Research question:** {question}",
        f"**Condition filter:** {condition or 'All conditions'}",
        f"**Generated:** {timestamp}",
        f"**Evidence passages selected:** {len(evidence)}", "",
        "## Summary", "",
        (
            "This report combines retrieved passages with a transparent, "
            "rule-based overview of terms and limitations mentioned in those "
            "passages. The synthesis is a navigation aid, not an independently "
            "verified systematic review or a substitute for reading the full papers."
        ), "",
        "## Cross-paper overview", "",
        f"The selected evidence contains passages from **{len(synthesis['papers'])} distinct paper ID(s)**.", "",
    ]

    if synthesis["papers"]:
        for paper_id, items in synthesis["papers"].items():
            citations = ", ".join(dict.fromkeys(_source_label(item) for item in items))
            lines.append(f"- **{paper_id}:** {len(items)} selected passage(s) ({citations}).")
        lines.append("")

    lines.extend(["## Imaging modalities mentioned", ""])
    _format_term_section(lines, "Detected modalities", synthesis["modalities"])
    lines.extend(["## Machine-learning methods mentioned", ""])
    _format_term_section(lines, "Detected methods", synthesis["models"])

    lines.extend(["## Candidate research gaps and limitations", ""])
    if not synthesis["candidate_gaps"]:
        lines.extend([
            "No candidate gap cues were detected in the selected passages. This does not mean the literature has no gaps; the retrieval may not have surfaced them.", ""
        ])
    else:
        for gap in synthesis["candidate_gaps"]:
            citations = ", ".join(dict.fromkeys(_source_label(item) for item in gap["evidence"]))
            lines.append(f"- **{gap['topic']}:** cues found in {citations}. {gap['note']}")
        lines.append("")

    lines.extend([
        "## Interpretation notes", "",
        "- A detected term means that it appears in a selected passage; it does not establish that a method is effective or clinically recommended.",
        "- Candidate gaps are inferred from limitations or future-work language in the selected passages, not from a comprehensive review of all 25 PDFs.",
        "- Verify every claim against the complete source paper and its methods/results before using it in academic work.", "",
    ])

    if not evidence:
        lines.extend([
            "## Retrieved evidence", "",
            "No passages passed the current reference-list filter.", "",
            "Try a more specific question, inspect the indexed PDFs, or review the filter if it appears to reject useful text.", "",
        ])
    else:
        lines.extend(["## Retrieved evidence", ""])
        for item in evidence:
            rank = item.get("rank", "?")
            paper_id = item.get("paper_id", "Unknown paper")
            page = item.get("page", "Unknown")
            condition_name = item.get("condition", "Unknown")
            source_file = item.get("source_file", "Unknown source")
            distance = item.get("cosine_distance")
            passage = item.get("passage", "").strip()
            lines.extend([
                f"### Evidence {rank}: {paper_id}", "",
                f"- **Condition:** {condition_name}",
                f"- **Page:** {page}",
                f"- **Source file:** {source_file}",
            ])
            if distance is not None:
                lines.append(f"- **Cosine distance:** {distance}")
            warnings = item.get("review_warnings", [])
            lines.append("- **Review warnings:** " + ("; ".join(warnings) if warnings else "None detected"))
            lines.extend([
                "", "**Retrieved passage:**", "", passage or "_No passage text available._", "",
                "**Verification note:** Confirm that the passage supports the claim you intend to make.", "", "---", "",
            ])

    lines.extend([
        "## Limitations", "",
        "- Reference detection relies on text-based heuristics and can make mistakes.",
        "- Retrieval relevance does not guarantee factual accuracy or complete coverage.",
        "- The synthesis uses keyword/rule matching; it does not deeply interpret context, resolve contradictions, or prove causal relationships.",
        "- Research gaps are candidates based only on the selected passages and require full-paper review.", "",
    ])
    return "\n".join(lines)


def save_outputs(question, evidence, condition=None, name=None):
    """Save the Markdown report and evidence JSON."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    if name:
        safe_name = re.sub(
            r"[^A-Za-z0-9_-]+",
            "_",
            name,
        ).strip("_")
    else:
        safe_name = "research_report"

    if not safe_name:
        safe_name = "research_report"

    report_path = OUTPUT_DIR / f"{safe_name}.md"
    evidence_path = OUTPUT_DIR / f"{safe_name}_evidence.json"

    report = make_report(
        question=question,
        evidence=evidence,
        condition=condition,
    )

    report_path.write_text(report, encoding="utf-8")

    evidence_data = {
        "question": question,
        "condition": condition,
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "evidence_count": len(evidence),
        "evidence": evidence,
        "synthesis": {
            "modalities": {
                key: [_source_label(item) for item in items]
                for key, items in synthesize_evidence(question, evidence)["modalities"].items()
            },
            "models": {
                key: [_source_label(item) for item in items]
                for key, items in synthesize_evidence(question, evidence)["models"].items()
            },
            "candidate_gaps": [
                {
                    "topic": gap["topic"],
                    "sources": list(dict.fromkeys(_source_label(item) for item in gap["evidence"])),
                    "note": gap["note"],
                }
                for gap in synthesize_evidence(question, evidence)["candidate_gaps"]
            ],
            "method": "rule-based keyword matching; verify against full papers",
        },
        "limitations": [
            "Retrieved passages are not independently fact-checked.",
            "Reference detection uses heuristics and can make mistakes.",
            "The selected passages may not cover all relevant papers.",
            "Synthesis and candidate gaps use rule-based matching, not deep semantic interpretation.",
        ],
    }

    with evidence_path.open("w", encoding="utf-8") as file:
        json.dump(
            evidence_data,
            file,
            indent=4,
            ensure_ascii=False,
            default=str,
        )

    return report_path, evidence_path


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Retrieve literature evidence and create a Markdown report "
            "and a JSON evidence file."
        )
    )

    parser.add_argument(
        "--question",
        type=str,
        required=True,
        help="Research question to investigate.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Maximum number of evidence passages to include.",
    )

    parser.add_argument(
        "--condition",
        type=str,
        default=None,
        choices=VALID_CONDITIONS,
        help="Optional condition filter.",
    )

    parser.add_argument(
        "--name",
        type=str,
        default=None,
        help="Optional output filename prefix.",
    )

    args = parser.parse_args()

    if args.top_k < 1:
        parser.error("--top-k must be at least 1.")

    print("\nNeuro Literature Research Copilot")
    print("=" * 40)
    print(f"Question: {args.question}")
    print(f"Condition: {args.condition or 'All conditions'}")
    print(f"Maximum evidence passages: {args.top_k}")
    print("\nRetrieving and assessing passages...")

    try:
        evidence = prepare_evidence(
            question=args.question,
            top_k=args.top_k,
            condition=args.condition,
        )

        report_path, evidence_path = save_outputs(
            question=args.question,
            evidence=evidence,
            condition=args.condition,
            name=args.name,
        )

        print("\nResearch completed.")
        print(f"Clean passages selected: {len(evidence)}")
        print(f"Markdown report: {report_path}")
        print(f"Evidence JSON: {evidence_path}")

        if len(evidence) < args.top_k:
            print(
                "\nNote: Fewer passages passed the filter than requested. "
                "The program did not fill the remaining slots with "
                "passages flagged as reference-heavy."
            )

        print(
            "\nPlease manually check the selected passages for relevance "
            "and scientific support."
        )

    except Exception as error:
        print(f"\nError while running research: {error}")
        raise


if __name__ == "__main__":
    main()
