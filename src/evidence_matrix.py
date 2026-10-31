
import csv
import json
import re
from pathlib import Path

# Project paths
ROOT = Path(__file__).resolve().parent.parent
CHUNKS_FILE = ROOT / "data" / "processed" / "chunks.jsonl"
OUTPUT_FILE = ROOT / "outputs" / "evidence_candidates.csv"

# Keywords are used to identify candidate evidence.
# A match is a clue for review, not proof of a scientific claim.
PATTERNS = {
    "dataset": [
        r"\bADNI\b",
        r"\bPPMI\b",
        r"\bOASIS\b",
        r"\bAIBL\b",
        r"\bHCP\b",
        r"\bNEUROCON\b",
        r"\bTao Wu\b",
        r"\bdataset\b",
        r"\bcohort\b",
        r"\bparticipants\b",
        r"\bpatients\b",
        r"\bsubjects\b",
    ],
    "modality": [
        r"\bMRI\b",
        r"\bfMRI\b",
        r"\brs-fMRI\b",
        r"\bDTI\b",
        r"\bPET\b",
        r"\bFDG-PET\b",
        r"\bFLAIR\b",
        r"\bT1[- ]weighted\b",
        r"\bEEG\b",
        r"\bMEG\b",
    ],
    "model": [
        r"\bCNN\b",
        r"\bConvKAN\b",
        r"\bGCN\b",
        r"\bSVM\b",
        r"\bLDA\b",
        r"\bRandom Forest\b",
        r"\bResNet\b",
        r"\bDenseNet\b",
        r"\bclassifier\b",
        r"\bdeep learning\b",
        r"\bneural network\b",
    ],
    "metric": [
        r"\baccuracy\b",
        r"\bprecision\b",
        r"\brecall\b",
        r"\bsensitivity\b",
        r"\bspecificity\b",
        r"\bF1(?:[- ]score)?\b",
        r"\bAUC\b",
        r"\bROC[- ]AUC\b",
        r"\bDice\b",
        r"\bIoU\b",
        r"\bconfidence interval\b",
    ],
    "validation": [
        r"\bcross[- ]validation\b",
        r"\bhold[- ]out\b",
        r"\bindependent cohort\b",
        r"\bindependent test\b",
        r"\bexternal validation\b",
        r"\btest set\b",
        r"\btraining set\b",
        r"\bleave[- ]one[- ]out\b",
        r"\bmulticenter\b",
        r"\bexternal dataset\b",
    ],
    "result": [
        r"\boutperformed\b",
        r"\bsignificant(?:ly)?\b",
        r"\bimproved\b",
        r"\bachieved\b",
        r"\bresult(?:s|ed)?\b",
        r"\bperformance\b",
        r"\b\d+(?:\.\d+)?\s*%",
        r"\b(?:accuracy|sensitivity|specificity|recall|precision|AUC|F1)\s*(?:=|:|of)?\s*0?\.\d+",
    ],
    "limitation": [
        r"\blimitation(?:s)?\b",
        r"\blimited\b",
        r"\bfuture work\b",
        r"\bfurther research\b",
        r"\bsmall sample\b",
        r"\bsmall cohort\b",
        r"\bgeneralizability\b",
        r"\bgeneralisation\b",
        r"\bbias\b",
        r"\bnot statistically significant\b",
        r"\bhowever\b",
    ],
}

# Common signs that a passage may be from a bibliography.
REFERENCE_PATTERNS = [
    r"\bdoi\s*:",
    r"\bhttps?://doi\.org/",
    r"\bet al\.",
    r"\bvol\.\s*\d+",
    r"\bpp\.\s*\d+",
    r"\bjournal\b",
]


def find_matches(text, patterns):
    """Return the actual matched keywords or phrases."""
    matches = []

    for pattern in patterns:
        for match in re.finditer(pattern, text, flags=re.IGNORECASE):
            value = match.group(0)
            if value.lower() not in [item.lower() for item in matches]:
                matches.append(value)

    return matches


def assess_reference_likelihood(text):
    """Flag likely bibliography content without deleting it."""
    lower_text = text.lower()
    score = 0

    if re.search(r"^\s*(references|bibliography)\s*$", lower_text):
        score += 3

    for pattern in REFERENCE_PATTERNS:
        if re.search(pattern, text, flags=re.IGNORECASE):
            score += 1

    # Many numbered citation entries may indicate a reference list.
    numbered_entries = len(
        re.findall(r"(?m)^\s*\[?\d{1,3}\]?[.)]\s+\S", text)
    )
    if numbered_entries >= 3:
        score += 2

    if score >= 3:
        return "high"
    if score >= 1:
        return "possible"
    return "low"


def main():
    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(
            f"Could not find {CHUNKS_FILE}\n"
            "Run the ingestion script first: python -m src.ingest"
        )

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    rows = []
    total_chunks = 0

    with CHUNKS_FILE.open("r", encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue

            chunk = json.loads(line)
            total_chunks += 1
            text = chunk.get("text", "")

            # Identify candidate evidence categories.
            categories = []
            matched_terms = []

            for category, patterns in PATTERNS.items():
                matches = find_matches(text, patterns)
                if matches:
                    categories.append(category)
                    matched_terms.extend(
                        f"{category}:{term}" for term in matches
                    )

            reference_likelihood = assess_reference_likelihood(text)

            # A simple prioritization aid, not a scientific confidence score.
            review_priority = "low"
            if categories and reference_likelihood == "low":
                review_priority = "medium"

            if (
                "metric" in categories
                and ("result" in categories or "validation" in categories)
                and reference_likelihood == "low"
            ):
                review_priority = "high"

            rows.append({
                "chunk_id": chunk.get("chunk_id", ""),
                "paper_id": chunk.get("paper_id", ""),
                "condition": chunk.get("condition", ""),
                "condition_key": chunk.get("condition_key", ""),
                "source_file": chunk.get("source_file", ""),
                "page": chunk.get("page", ""),
                "chunk_index_on_page": chunk.get(
                    "chunk_index_on_page", ""
                ),
                "evidence_categories": "; ".join(categories),
                "matched_terms": "; ".join(matched_terms),
                "reference_likelihood": reference_likelihood,
                "review_priority": review_priority,
                "text": text,
            })

    fieldnames = [
        "chunk_id",
        "paper_id",
        "condition",
        "condition_key",
        "source_file",
        "page",
        "chunk_index_on_page",
        "evidence_categories",
        "matched_terms",
        "reference_likelihood",
        "review_priority",
        "text",
    ]

    with OUTPUT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print("\nEvidence candidate extraction complete.")
    print(f"Chunks processed: {total_chunks}")
    print(f"Rows written: {len(rows)}")
    print(f"Output file: {OUTPUT_FILE}")

    print("\nCandidate category counts:")
    for category in PATTERNS:
        count = sum(
            category in row["evidence_categories"].split("; ")
            for row in rows
        )
        print(f"  {category}: {count}")

    print("\nReview priority counts:")
    for priority in ["high", "medium", "low"]:
        count = sum(
            row["review_priority"] == priority for row in rows
        )
        print(f"  {priority}: {count}")


if __name__ == "__main__":
    main()
