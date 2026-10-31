
import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CHUNKS_FILE = ROOT / "data" / "processed" / "chunks.jsonl"
OUTPUT_FILE = ROOT / "outputs" / "evidence_claims.csv"


# --------------------------------------------------
# 1. Candidate evidence patterns
# --------------------------------------------------

PATTERNS = {
    "dataset": re.compile(
        r"\b(ADNI|PPMI|OASIS|AIBL|HCP|NEUROCON|"
        r"dataset|cohort|subjects|patients|participants)\b",
        re.I,
    ),
    "modality": re.compile(
        r"\b(MRI|fMRI|sMRI|rs-fMRI|DTI|PET|EEG|MEG|"
        r"T1[- ]weighted|FLAIR|diffusion tensor imaging)\b",
        re.I,
    ),
    "model": re.compile(
        r"\b(CNN|VGG|ResNet|SVM|random forest|"
        r"XGBoost|LightGBM|GCN|ConvKAN|transformer|"
        r"deep learning|neural network|"
        r"convolutional neural network)\b",
        re.I,
    ),
    "metric": re.compile(
        r"\b(accuracy|AUC|AUROC|F1(?:-score)?|"
        r"precision|recall|sensitivity|specificity|"
        r"Dice(?: coefficient)?|IoU)\b",
        re.I,
    ),
    "validation": re.compile(
        r"\b(cross-validation|cross validation|"
        r"leave-one-out|independent cohort|"
        r"external validation|hold-out|held-out|"
        r"test set|testing set|testing cohort|"
        r"validation set)\b",
        re.I,
    ),
    "limitation": re.compile(
        r"\b(limitation|limitations|limited by|"
        r"future work|future studies|small sample|"
        r"generalizability|generalizability|"
        r"generalisation|generalization|"
        r"lack of|not generalizable|not generalisable)\b",
        re.I,
    ),
}

# Detect metric names followed by a nearby numerical value.
# This is a candidate detector, not a full table parser.
METRIC_VALUE = re.compile(
    r"\b(accuracy|AUC|AUROC|F1(?:-score)?|precision|"
    r"recall|sensitivity|specificity|Dice(?: coefficient)?|IoU)"
    r"\b[^.;\n]{0,45}?"
    r"(\d+(?:\.\d+)?\s*%?)",
    re.I,
)

RESULT_LANGUAGE = re.compile(
    r"\b(results?|achieved|outperformed|improved|"
    r"performance|higher|lower|significant|"
    r"demonstrated|showed|reported|found)\b",
    re.I,
)


# --------------------------------------------------
# 2. Load and normalize source chunks
# --------------------------------------------------

def load_chunks(path):
    chunks = []

    with open(path, encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            if not line.strip():
                continue

            try:
                item = json.loads(line)
                if isinstance(item, dict):
                    chunks.append(item)
                else:
                    print(
                        f"Warning: skipped non-object JSON "
                        f"on line {line_number}"
                    )
            except json.JSONDecodeError:
                print(
                    f"Warning: skipped invalid JSON "
                    f"on line {line_number}"
                )

    return chunks


def get_text(chunk):
    for key in ("text", "chunk_text", "content"):
        value = chunk.get(key)

        if isinstance(value, str) and value.strip():
            return value.strip()

    return ""


def get_value(chunk, *keys):
    for key in keys:
        value = chunk.get(key)

        if value is not None and str(value).strip():
            return str(value).strip()

    return ""


def split_sentences(text):
    """
    Simple sentence splitting.

    Scientific abbreviations, decimal numbers, and PDF formatting
    can create imperfect boundaries. Review extracted claims.
    """
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", text)

    return [
        part.strip()
        for part in parts
        if part.strip()
    ]


def detect_categories(sentence):
    return [
        category
        for category, pattern in PATTERNS.items()
        if pattern.search(sentence)
    ]


# --------------------------------------------------
# 3. Identify likely low-value text and assign priority
# --------------------------------------------------

def is_metadata(sentence):
    text = sentence.casefold()

    if "keywords:" in text or text.startswith("keywords "):
        return True

    # Likely author affiliation or institutional information.
    affiliation_terms = (
        "university",
        "school of",
        "department of",
        "faculty of",
        "institute of",
    )

    if (
        len(sentence) > 100
        and any(term in text for term in affiliation_terms)
        and not METRIC_VALUE.search(sentence)
    ):
        return True

    return False


def assign_priority(sentence, categories):
    """
    Heuristic review priority only.

    High does not mean correct, scientifically strong, or verified.
    """
    if is_metadata(sentence):
        return "low"

    has_metric = bool(METRIC_VALUE.search(sentence))
    has_validation = "validation" in categories
    has_limitation = "limitation" in categories
    has_dataset = "dataset" in categories
    has_result_language = bool(
        RESULT_LANGUAGE.search(sentence)
    )

    # Stronger candidates for manual review.
    if has_metric and has_result_language:
        return "high"

    if has_limitation:
        return "high"

    if has_dataset and has_validation:
        return "high"

    return "medium"


# --------------------------------------------------
# 4. Extract candidate claims
# --------------------------------------------------

def main():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Chunk file not found: {CHUNKS_FILE}\n"
            "Run the ingestion script first."
        )

    chunks = load_chunks(CHUNKS_FILE)

    claims = []
    seen = set()
    duplicate_count = 0
    empty_count = 0

    for chunk in chunks:
        text = get_text(chunk)

        if not text:
            empty_count += 1
            continue

        paper_id = get_value(chunk, "paper_id")
        condition = get_value(chunk, "condition")
        page = get_value(chunk, "page")
        chunk_id = get_value(chunk, "chunk_id", "id")

        sentences = split_sentences(text)

        for sentence in sentences:
            categories = detect_categories(sentence)

            if not categories:
                continue

            normalized = re.sub(
                r"\s+", " ", sentence
            ).strip()

            # Deduplicate identical sentences on the same page.
            # Keep page-level traceability.
            dedup_key = (
                paper_id,
                page,
                normalized.casefold(),
            )

            if dedup_key in seen:
                duplicate_count += 1
                continue

            seen.add(dedup_key)

            metric_matches = [
                f"{match.group(1)}: {match.group(2)}"
                for match in METRIC_VALUE.finditer(normalized)
            ]

            priority = assign_priority(
                normalized,
                categories,
            )

            claims.append({
                "claim_id": f"CLM{len(claims) + 1:05d}",
                "paper_id": paper_id,
                "condition": condition,
                "page": page,
                "chunk_id": chunk_id,
                "claim_categories": "; ".join(categories),
                "review_priority": priority,
                "metric_values_detected": "; ".join(
                    metric_matches
                ),
                "claim_text": normalized,
                "verification_status": "Needs review",
            })

    # --------------------------------------------------
    # 5. Write output CSV
    # --------------------------------------------------

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fieldnames = [
        "claim_id",
        "paper_id",
        "condition",
        "page",
        "chunk_id",
        "claim_categories",
        "review_priority",
        "metric_values_detected",
        "claim_text",
        "verification_status",
    ]

    with open(
        OUTPUT_FILE,
        "w",
        encoding="utf-8-sig",
        newline="",
    ) as f:
        writer = csv.DictWriter(
            f,
            fieldnames=fieldnames,
        )

        writer.writeheader()
        writer.writerows(claims)

    # --------------------------------------------------
    # 6. Report extraction summary
    # --------------------------------------------------

    priority_counts = {
        "high": 0,
        "medium": 0,
        "low": 0,
    }

    for claim in claims:
        priority_counts[claim["review_priority"]] += 1

    print("\nCandidate claim extraction complete.")
    print("Input chunks:", len(chunks))
    print("Candidate claims:", len(claims))
    print("Duplicate sentences skipped:", duplicate_count)
    print("Chunks with no text:", empty_count)

    print("\nReview priority counts:")
    for priority, count in priority_counts.items():
        print(f"  {priority}: {count}")

    print("\nOutput file:", OUTPUT_FILE)
    print(
        "\nIMPORTANT: These are automatically extracted "
        "candidate claims, not verified scientific findings."
    )


if __name__ == "__main__":
    main()
