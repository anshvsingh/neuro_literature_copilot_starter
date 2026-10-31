
import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

INPUT_FILE = ROOT / "outputs" / "evidence_claims.csv"
OUTPUT_FILE = ROOT / "outputs" / "evidence_claims_with_origin.csv"

# Signals that a claim may describe previously published research.
PRIOR_WORK_PATTERNS = [
    r"\bprevious(?:ly)?\b",
    r"\bprior work\b",
    r"\bearlier work\b",
    r"\bexisting (?:method|approach|model|study|research)\b",
    r"\bstate[- ]of[- ]the[- ]art\b",
    r"\bother studies\b",
    r"\banother study\b",
    r"\bthey achieved\b",
    r"\breported by\b",
    r"\b(?:proposed|developed|introduced|achieved|reported)\b.{0,100}"
    r"\b(?:et al\.?|[A-Z][a-z]+)\b",
    r"\baccording to\b",
    r"\bcompared with (?:the )?(?:previous|existing|earlier)\b",
]

# Signals that a claim may describe the current paper's work.
CURRENT_WORK_PATTERNS = [
    r"\bin this study\b",
    r"\bin this paper\b",
    r"\bin our study\b",
    r"\bour proposed\b",
    r"\bour model\b",
    r"\bour method\b",
    r"\bour results\b",
    r"\bwe propose\b",
    r"\bwe developed\b",
    r"\bwe trained\b",
    r"\bwe evaluated\b",
    r"\bwe achieved\b",
    r"\bwe obtained\b",
    r"\bwe used\b",
    r"\bthe proposed (?:method|model|approach|framework)\b",
    r"\bthe present study\b",
    r"\bexperimental results show\b",
    r"\bresults demonstrate\b",
]

# Explicit reference numbers often indicate cited work, but can also
# appear in descriptions of the current paper. They are only one signal.
REFERENCE_PATTERN = re.compile(
    r"\[\s*\d+(?:\s*[,–-]\s*\d+)*\s*\]"
)


def matches_any(text, patterns):
    return any(re.search(pattern, text, re.IGNORECASE)
               for pattern in patterns)


def classify_origin(row):
    text = row.get("claim_text", "").strip()

    if not text:
        return "uncertain"

    prior_signal = matches_any(text, PRIOR_WORK_PATTERNS)
    current_signal = matches_any(text, CURRENT_WORK_PATTERNS)
    has_reference = bool(REFERENCE_PATTERN.search(text))

    # A citation by itself is not enough to classify a claim as prior work.
    if prior_signal and not current_signal:
        return "likely_prior_work"

    # Conflicting signals require manual review.
    if prior_signal and current_signal:
        return "uncertain"

    # Current-study wording without strong prior-work wording.
    if current_signal:
        return "likely_current_study"

    # References alone are ambiguous, so leave these for review.
    if has_reference:
        return "uncertain"

    return "uncertain"


def main():
    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Input file not found: {INPUT_FILE}\n"
            "Run the claim extraction script first."
        )

    with INPUT_FILE.open(
        "r", encoding="utf-8-sig", newline=""
    ) as file:
        reader = csv.DictReader(file)
        rows = list(reader)
        fieldnames = list(reader.fieldnames or [])

    if "claim_text" not in fieldnames:
        raise ValueError(
            "The input CSV does not contain a 'claim_text' column."
        )

    if "evidence_origin" not in fieldnames:
        fieldnames.append("evidence_origin")

    counts = {
        "likely_prior_work": 0,
        "likely_current_study": 0,
        "uncertain": 0,
    }

    for row in rows:
        origin = classify_origin(row)
        row["evidence_origin"] = origin
        counts[origin] += 1

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with OUTPUT_FILE.open(
        "w", encoding="utf-8-sig", newline=""
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=fieldnames, extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(rows)

    print("Evidence-origin classification complete.")
    print(f"Input claims: {len(rows)}")
    print(f"Likely prior work: {counts['likely_prior_work']}")
    print(f"Likely current study: {counts['likely_current_study']}")
    print(f"Uncertain: {counts['uncertain']}")
    print(f"Output: {OUTPUT_FILE}")
    print("\nIMPORTANT:")
    print("These labels are heuristic suggestions, not verified facts.")
    print("Review the original claim text and source PDF before citing.")


if __name__ == "__main__":
    main()
