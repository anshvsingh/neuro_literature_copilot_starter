
import csv
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent

MANIFEST = ROOT / "data" / "processed" / "manifest.csv"
CANDIDATES = ROOT / "outputs" / "evidence_candidates.csv"
OUTPUT = ROOT / "outputs" / "paper_evidence_matrix.csv"

# Evidence categories to consolidate across chunks.
CATEGORIES = [
    "dataset",
    "modality",
    "model",
    "metric",
    "validation",
    "result",
    "limitation",
]

def read_csv(path):
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def unique_values(values):
    seen = set()
    output = []

    for value in values:
        value = (value or "").strip()
        if value and value not in seen:
            seen.add(value)
            output.append(value)

    return output

manifest = read_csv(MANIFEST)
candidates = read_csv(CANDIDATES)

# Start with every paper in the manifest, including papers
# for which no evidence candidates were extracted.
papers = {
    row["paper_id"]: {
        **row,
        "chunks": [],
    }
    for row in manifest
}

for chunk in candidates:
    paper_id = chunk.get("paper_id", "").strip()

    if paper_id in papers:
        papers[paper_id]["chunks"].append(chunk)

OUTPUT.parent.mkdir(parents=True, exist_ok=True)

fieldnames = [
    "paper_id",
    "condition",
    "condition_key",
    "title",
    "authors",
    "year",
    "doi",
    "pdf_path",
    "page_count",
    "parse_status",
    "candidate_chunk_count",
    "dataset_evidence",
    "modality_evidence",
    "model_evidence",
    "metric_evidence",
    "validation_evidence",
    "result_evidence",
    "limitation_evidence",
    "source_pages",
    "verification_status",
]

with open(OUTPUT, "w", encoding="utf-8-sig", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()

    for paper_id, paper in sorted(papers.items()):
        chunks = paper["chunks"]

        row = {
            key: paper.get(key, "")
            for key in fieldnames
        }

        row["candidate_chunk_count"] = len(chunks)

        for category in CATEGORIES:
            matching_texts = []

            for chunk in chunks:
                categories = {
                    item.strip()
                    for item in chunk.get(
                        "evidence_categories", ""
                    ).split(";")
                }

                if category in categories:
                    text = chunk.get("text", "").strip()
                    page = chunk.get("page", "").strip()

                    if text:
                        matching_texts.append(
                            f"[Page {page}] {text}"
                        )

            row[f"{category}_evidence"] = "\n\n".join(
                unique_values(matching_texts)
            )

        pages = unique_values(
            chunk.get("page", "") for chunk in chunks
        )
        row["source_pages"] = "; ".join(pages)

        row["verification_status"] = "Needs review"

        writer.writerow(row)

print("Paper-level evidence matrix created.")
print("Papers in manifest:", len(manifest))
print("Papers in output:", len(papers))
print("Output:", OUTPUT)
print("\nAll rows are candidate evidence, not verified findings.")
