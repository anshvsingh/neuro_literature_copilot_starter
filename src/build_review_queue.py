
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "outputs" / "evidence_claims_with_origin.csv"
OUTPUT_FILE = ROOT / "outputs" / "evidence_review_queue.csv"

# Terms that help identify claims worth reviewing.
RESULT_PATTERN = re.compile(
    r"\b(accuracy|sensitivity|specificity|precision|recall|"
    r"f1[- ]?score|auc|area under the curve|dice|iou|"
    r"p[- ]?value|confidence interval|mean absolute error|"
    r"rmse|roc[- ]?auc|outperformed|outperforming|"
    r"significant improvement|achieved|obtained)\b",
    re.IGNORECASE,
)

DATASET_PATTERN = re.compile(
    r"\b(dataset|database|cohort|subjects|patients|participants|"
    r"adni|ppmi|neurocon|training set|test set|validation set)\b",
    re.IGNORECASE,
)

METHOD_PATTERN = re.compile(
    r"\b(cnn|convolutional neural network|transformer|"
    r"random forest|support vector machine|svm|"
    r"neural network|classifier|classification|"
    r"segmentation|mri|fmri|functional connectivity|"
    r"diffusion tensor imaging|dti|pet|eeg|meg)\b",
    re.IGNORECASE,
)

VALIDATION_PATTERN = re.compile(
    r"\b(cross[- ]validation|cross validation|"
    r"hold[- ]out|held[- ]out|independent test|"
    r"external validation|train(?:ing)? set|test set|"
    r"validation set|patient[- ]level split|"
    r"data leakage)\b",
    re.IGNORECASE,
)

LIMITATION_PATTERN = re.compile(
    r"\b(limitation|limitations|limited by|limiting factor|"
    r"future work|future research|small sample|"
    r"small dataset|generalizability|generalisation|"
    r"generalization|bias|overfitting|not significant|"
    r"lack of|unable to|cannot be)\b",
    re.IGNORECASE,
)


def calculate_score(row):
    text = row.get("claim_text", "").strip()
    categories = row.get("claim_categories", "").lower()
    origin = row.get("evidence_origin", "uncertain")

    score = 0
    reasons = []

    if RESULT_PATTERN.search(text):
        score += 3
        reasons.append("possible_result_or_metric")

    if DATASET_PATTERN.search(text) or "dataset" in categories:
        score += 2
        reasons.append("dataset_evidence")

    if VALIDATION_PATTERN.search(text) or "validation" in categories:
        score += 2
        reasons.append("validation_evidence")

    if LIMITATION_PATTERN.search(text) or "limitation" in categories:
        score += 2
        reasons.append("limitation_evidence")

    if METHOD_PATTERN.search(text) or "model" in categories:
        score += 1
        reasons.append("method_or_modality")

    if origin == "likely_current_study":
        score += 1
        reasons.append("possible_current_study")

    elif origin == "likely_prior_work":
        reasons.append("check_prior_work_attribution")

    # Long text can contain several statements and deserves careful review.
    if len(text) > 500:
        reasons.append("long_claim_check_segmentation")

    if len(text) > 1000:
        score -= 2

    return score, "; ".join(reasons) if reasons else "general_candidate"



# Conservative duplicate detection: flag matching result signatures
# within the same paper. This is a review aid, not proof of duplication.
DUPLICATE_SIGNATURE_PATTERN = re.compile(
    r"(?P<dataset>\b(?:PPMI|ADNI|NEUROCON|Tao Wu)\b)"
    r".{0,180}?"
    r"(?P<model>\b(?:3D\s+ConvKAN|2D\s+ConvKAN|3D\s+CNN|2D\s+CNN|"
    r"ConvKAN|CNN|GCN)\b)"
    r".{0,180}?"
    r"(?:accuracy\s*[:=]?\s*(?P<accuracy>0?\.\d+))?"
    r".{0,120}?"
    r"(?:AUC\s*[:=]?\s*(?P<auc>0?\.\d+))?",
    re.IGNORECASE | re.DOTALL,
)


def duplicate_signature(text):
    text = text or ""

    dataset_match = re.search(
        r"\b(PPMI|ADNI|NEUROCON|Tao Wu)\b",
        text,
        re.IGNORECASE,
    )

    model_match = re.search(
        r"\b(3D\s+ConvKAN|2D\s+ConvKAN|3D\s+CNN|"
        r"2D\s+CNN|3D\s+GCN|2D\s+GCN|ConvKAN|CNN|GCN)\b",
        text,
        re.IGNORECASE,
    )

    accuracy_match = re.search(
        r"\baccuracy\s*(?:of\s*)?[:=]?\s*(0?\.\d+)",
        text,
        re.IGNORECASE,
    )

    auc_match = re.search(
        r"\bAUC\s*(?:of\s*)?[:=]?\s*(0?\.\d+)",
        text,
        re.IGNORECASE,
    )

    if not (
        dataset_match
        and model_match
        and (accuracy_match or auc_match)
    ):
        return ""

    if re.search(
         r"hold[- ]out|held[- ]out|generalization capabilities|"
         r"generalization to early[- ]stage",
         text,
         re.IGNORECASE,
    ):
         experiment = "holdout"
    elif re.search(
         r"isolated dataset|isolated analysis",
         text,
         re.IGNORECASE,
    ):
         experiment = "isolated"
    else:
         experiment = "unspecified"

    dataset = dataset_match.group(1).upper()
    model = re.sub(r"\s+", "", model_match.group(1)).upper()
    accuracy = accuracy_match.group(1) if accuracy_match else "NA"
    auc = auc_match.group(1) if auc_match else "NA"

    return (
        f"{dataset}|{model}|{experiment}|"
        f"ACC:{accuracy}|AUC:{auc}"
    )


def normalized_claim(text):
    text = re.sub(r"\s+", " ", (text or "").lower()).strip()
    return re.sub(r"[^a-z0-9.]+", " ", text).strip()


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}\n"
            "Run the evidence-origin classification script first."
        )

    with INPUT_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        original_fields = list(reader.fieldnames or [])

    required = {
        "claim_id",
        "paper_id",
        "condition",
        "page",
        "claim_text",
        "evidence_origin",
    }

    missing = required - set(original_fields)
    if missing:
        raise ValueError(
            f"Missing required columns: {', '.join(sorted(missing))}"
        )

    output_rows = []
    exact_counts = {}
    signature_counts = {}

    for row in rows:
        exact_key = (row.get("paper_id", ""), normalized_claim(row.get("claim_text", "")))
        if exact_key[1]:
            exact_counts[exact_key] = exact_counts.get(exact_key, 0) + 1

        signature = duplicate_signature(row.get("claim_text", ""))
        signature_key = (row.get("paper_id", ""), signature)
        if signature:
            signature_counts[signature_key] = signature_counts.get(signature_key, 0) + 1

    for row in rows:
        score, reasons = calculate_score(row)
        exact_key = (row.get("paper_id", ""), normalized_claim(row.get("claim_text", "")))
        signature = duplicate_signature(row.get("claim_text", ""))
        signature_key = (row.get("paper_id", ""), signature)

        duplicate_flags = []
        if exact_key[1] and exact_counts.get(exact_key, 0) > 1:
            duplicate_flags.append("possible_exact_duplicate_same_paper")
        if signature and signature_counts.get(signature_key, 0) > 1:
            duplicate_flags.append("possible_repeated_result_signature")

        output_rows.append({
            "review_rank": 0,
            "claim_id": row.get("claim_id", ""),
            "paper_id": row.get("paper_id", ""),
            "condition": row.get("condition", ""),
            "page": row.get("page", ""),
            "claim_categories": row.get("claim_categories", ""),
            "review_priority_original": row.get("review_priority", ""),
            "evidence_origin": row.get("evidence_origin", "uncertain"),
            "review_score": score,
            "review_reasons": reasons,
            "duplicate_flag": "; ".join(duplicate_flags) if duplicate_flags else "",
            "duplicate_signature": signature,
            "verification_status": row.get(
                "verification_status", "unverified"
            ),
            "claim_text": row.get("claim_text", ""),
        })

    # Higher scores appear first; claim IDs provide stable tie-breaking.
    output_rows.sort(
        key=lambda row: (
            -row["review_score"],
            row["paper_id"],
            row["claim_id"],
        )
    )

    for rank, row in enumerate(output_rows, start=1):
        row["review_rank"] = rank

    fieldnames = [
        "review_rank",
        "claim_id",
        "paper_id",
        "condition",
        "page",
        "claim_categories",
        "review_priority_original",
        "evidence_origin",
        "review_score",
        "review_reasons",
        "duplicate_flag",
        "duplicate_signature",
        "verification_status",
        "claim_text",
    ]

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(output_rows)

    print("Evidence review queue created.")
    print(f"Claims ranked: {len(output_rows)}")
    print(f"Output: {OUTPUT_FILE}")

    print("\nTop 10 candidates:")
    for row in output_rows[:10]:
        text = row["claim_text"].replace("\n", " ")
        print(
            f"\nRank {row['review_rank']} | {row['claim_id']} | "
            f"{row['paper_id']} | page {row['page']} | "
            f"score {row['review_score']}"
        )
        print(f"Origin: {row['evidence_origin']}")
        print(f"Reasons: {row['review_reasons']}")
        print(f"Claim: {text[:300]}")

    print(
        "\nReminder: review scores are heuristic ranking signals, "
        "not scientific confidence scores."
    )


if __name__ == "__main__":
    main()
