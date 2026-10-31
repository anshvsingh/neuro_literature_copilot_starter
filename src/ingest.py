"""Extract text from the curated PDF corpus and write page-aware chunks.

Run from the project root: python -m src.ingest
"""
from __future__ import annotations
import csv, json, re
from pathlib import Path
from typing import Iterator
import fitz

ROOT = Path(__file__).resolve().parents[1]
PAPERS_DIR = ROOT / "data" / "papers"
PROCESSED_DIR = ROOT / "data" / "processed"
MANIFEST_PATH = PROCESSED_DIR / "manifest.csv"
CHUNKS_PATH = PROCESSED_DIR / "chunks.jsonl"
CONDITIONS = {
    "alzheimers": "Alzheimer's disease",
    "epilepsy": "Epilepsy",
    "parkinsons": "Parkinson's disease",
    "schizophrenia": "Schizophrenia",
}
PREFIXES = {"alzheimers": "ALZ", "epilepsy": "EPI", "parkinsons": "PAR", "schizophrenia": "SCH"}
CHUNK_WORDS, OVERLAP_WORDS = 220, 40

def clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\\x00", " ")).strip()

def split_words(text: str, chunk_words: int = CHUNK_WORDS, overlap_words: int = OVERLAP_WORDS) -> Iterator[str]:
    words = text.split()
    start = 0
    while start < len(words):
        end = min(start + chunk_words, len(words))
        chunk = " ".join(words[start:end]).strip()
        if chunk:
            yield chunk
        if end >= len(words):
            break
        start = max(end - overlap_words, start + 1)

def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    manifest_rows, chunk_rows = [], []
    for key, label in CONDITIONS.items():
        pdfs = sorted((PAPERS_DIR / key).glob("*.pdf"), key=lambda p: p.name.lower())
        if not pdfs:
            print(f"[WARN] No PDFs found in data/papers/{key}/")
        for idx, pdf_path in enumerate(pdfs, start=1):
            paper_id = f"{PREFIXES[key]}{idx:02d}"
            pages_with_text = chars = 0
            errors, page_count = [], ""
            try:
                with fitz.open(pdf_path) as doc:
                    page_count = len(doc)
                    for page_idx, page in enumerate(doc):
                        text = clean_text(page.get_text("text"))
                        if not text:
                            continue
                        pages_with_text += 1
                        chars += len(text)
                        for chunk_idx, chunk in enumerate(split_words(text), start=1):
                            chunk_rows.append({
                                "chunk_id": f"{paper_id}_pg{page_idx+1:03d}_ch{chunk_idx:03d}",
                                "paper_id": paper_id, "condition": label, "condition_key": key,
                                "source_file": str(pdf_path.relative_to(ROOT)),
                                "page": page_idx + 1, "chunk_index_on_page": chunk_idx, "text": chunk
                            })
                status = "ok" if chars else "no_text_extracted"
                if not chars:
                    errors.append("No selectable text; OCR may be needed.")
            except Exception as exc:
                status = "error"
                errors.append(f"{type(exc).__name__}: {exc}")
            paper_chunks = sum(1 for c in chunk_rows if c["paper_id"] == paper_id)
            manifest_rows.append({
                "paper_id": paper_id, "condition": label, "condition_key": key,
                "title": "", "authors": "", "year": "", "doi": "", "source_url": "",
                "pdf_path": str(pdf_path.relative_to(ROOT)), "page_count": page_count,
                "pages_with_text": pages_with_text, "extracted_characters": chars,
                "chunk_count": paper_chunks, "parse_status": status, "notes": " | ".join(errors)
            })
            print(f"[{status.upper()}] {paper_id}: {pdf_path.name} ({pages_with_text} pages with text)")
    fields = ["paper_id","condition","condition_key","title","authors","year","doi","source_url",
              "pdf_path","page_count","pages_with_text","extracted_characters","chunk_count","parse_status","notes"]
    with MANIFEST_PATH.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(manifest_rows)
    with CHUNKS_PATH.open("w", encoding="utf-8") as f:
        for row in chunk_rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    print("\n=== INGESTION SUMMARY ===")
    print(f"PDFs found: {len(manifest_rows)}")
    for key, label in CONDITIONS.items():
        print(f"{label}: {sum(1 for r in manifest_rows if r['condition_key'] == key)}")
    print(f"Chunks written: {len(chunk_rows)}")
    print(f"Manifest: {MANIFEST_PATH.relative_to(ROOT)}")
    print(f"Chunks: {CHUNKS_PATH.relative_to(ROOT)}")
    if len(manifest_rows) != 25:
        print("[NEXT STEP] Expected 25 PDFs. Check the folder counts.")

if __name__ == "__main__":
    main()
