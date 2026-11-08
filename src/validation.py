"""Citation and source-page validation module for Neuro Literature Research Copilot.

Provides robust validation of:
- Citation format strings (e.g., 'ALZ01, p. 4', 'PAR07, pp. 2-4')
- Paper ID validity and existence against the corpus manifest
- Source page boundaries per paper
- Evidence item structural integrity and text groundedness
- Automated auditing of citations in generated Markdown reports
"""

import csv
import json
import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "data" / "processed" / "manifest.csv"
CHUNKS_PATH = ROOT / "data" / "processed" / "chunks.jsonl"
PAPERS_DIR = ROOT / "data" / "papers"

# Known canonical paper bounds fallback if manifest is not yet generated
DEFAULT_PAPER_PAGES = {
    "ALZ01": 5, "ALZ02": 5, "ALZ03": 6, "ALZ04": 6, "ALZ05": 10, "ALZ06": 46,
    "EPI01": 5, "EPI02": 6, "EPI03": 12, "EPI04": 8, "EPI05": 6,
    "PAR01": 6, "PAR02": 16, "PAR03": 6, "PAR04": 6, "PAR05": 6, "PAR06": 16, "PAR07": 8, "PAR08": 12,
    "SCH01": 6, "SCH02": 6, "SCH03": 5, "SCH04": 5, "SCH05": 5, "SCH06": 5,
}

_MANIFEST_CACHE: Optional[Dict[str, Dict[str, Any]]] = None


def load_manifest(manifest_path: Optional[Path] = None) -> Dict[str, Dict[str, Any]]:
    """Load and cache the paper manifest mapping paper_id to metadata."""
    global _MANIFEST_CACHE
    if _MANIFEST_CACHE is not None and manifest_path is None:
        return _MANIFEST_CACHE

    target_path = manifest_path or MANIFEST_PATH
    manifest_data = {}

    if target_path.exists():
        with target_path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pid = row.get("paper_id", "").strip().upper()
                if pid:
                    try:
                        page_count = int(row.get("page_count", 0))
                    except (ValueError, TypeError):
                        page_count = DEFAULT_PAPER_PAGES.get(pid, 1)
                    manifest_data[pid] = {
                        "paper_id": pid,
                        "condition": row.get("condition", ""),
                        "condition_key": row.get("condition_key", ""),
                        "page_count": page_count,
                        "pdf_path": row.get("pdf_path", ""),
                    }
    else:
        # Fallback to known corpus papers
        for pid, pcount in DEFAULT_PAPER_PAGES.items():
            manifest_data[pid] = {
                "paper_id": pid,
                "page_count": pcount,
            }

    if manifest_path is None:
        _MANIFEST_CACHE = manifest_data
    return manifest_data


def validate_citation_format(citation_str: str) -> Dict[str, Any]:
    """
    Validate and parse a citation string.
    
    Accepts formats such as:
      - 'ALZ01, p. 4'
      - 'EPI03, p. 11'
      - 'PAR07, pp. 2-4'
      - 'SCH04, p. 2'
    """
    if not isinstance(citation_str, str) or not citation_str.strip():
        return {
            "is_valid": False,
            "paper_id": None,
            "page": None,
            "raw": citation_str,
            "error": "Citation string is empty or not a string",
        }

    raw = citation_str.strip()
    # Match paper ID and single page: ALZ01, p. 4 or ALZ01, p.4
    single_match = re.match(r"^([A-Z]{2,4}\d{2})\s*,\s*p\.\s*(\d+)$", raw, re.IGNORECASE)
    if single_match:
        return {
            "is_valid": True,
            "paper_id": single_match.group(1).upper(),
            "page": int(single_match.group(2)),
            "raw": raw,
            "error": None,
        }

    # Match paper ID and page range: ALZ01, pp. 2-4
    range_match = re.match(r"^([A-Z]{2,4}\d{2})\s*,\s*pp\.\s*(\d+)\s*[-–]\s*(\d+)$", raw, re.IGNORECASE)
    if range_match:
        start_pg = int(range_match.group(2))
        end_pg = int(range_match.group(3))
        if end_pg < start_pg:
            return {
                "is_valid": False,
                "paper_id": range_match.group(1).upper(),
                "page": None,
                "raw": raw,
                "error": f"Invalid page range: start page {start_pg} > end page {end_pg}",
            }
        return {
            "is_valid": True,
            "paper_id": range_match.group(1).upper(),
            "page": list(range(start_pg, end_pg + 1)),
            "raw": raw,
            "error": None,
        }

    return {
        "is_valid": False,
        "paper_id": None,
        "page": None,
        "raw": raw,
        "error": f"Citation string '{raw}' does not match expected format 'PAPER_ID, p. PAGE' or 'PAPER_ID, pp. START-END'",
    }


def validate_source_page(paper_id: str, page: int, manifest: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Validate whether a paper_id exists in the corpus and whether page is within bounds.
    """
    papers = manifest if manifest is not None else load_manifest()
    norm_id = str(paper_id).strip().upper()

    if norm_id not in papers:
        return {
            "is_valid": False,
            "paper_id": norm_id,
            "page": page,
            "max_pages": None,
            "error": f"Paper ID '{norm_id}' not found in manifest. Known papers: {sorted(papers.keys())}",
        }

    try:
        page_num = int(page)
    except (TypeError, ValueError):
        return {
            "is_valid": False,
            "paper_id": norm_id,
            "page": page,
            "max_pages": papers[norm_id].get("page_count"),
            "error": f"Page '{page}' is not a valid integer",
        }

    max_pages = papers[norm_id].get("page_count", 0)
    if page_num < 1:
        return {
            "is_valid": False,
            "paper_id": norm_id,
            "page": page_num,
            "max_pages": max_pages,
            "error": f"Page number {page_num} must be >= 1",
        }

    if max_pages > 0 and page_num > max_pages:
        return {
            "is_valid": False,
            "paper_id": norm_id,
            "page": page_num,
            "max_pages": max_pages,
            "error": f"Page number {page_num} exceeds max page count {max_pages} for paper '{norm_id}'",
        }

    return {
        "is_valid": True,
        "paper_id": norm_id,
        "page": page_num,
        "max_pages": max_pages,
        "error": None,
    }


def validate_evidence_item(item: Dict[str, Any], manifest: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Validate a single evidence dictionary for structure, paper validity, and page limits.
    """
    errors = []
    paper_id = item.get("paper_id")
    page = item.get("page")
    passage = item.get("passage") or item.get("quote")

    if not paper_id:
        errors.append("Missing 'paper_id'")
    if page is None:
        errors.append("Missing 'page'")
    if not passage:
        errors.append("Missing passage or quote text")

    if paper_id and page is not None:
        page_val = validate_source_page(str(paper_id), page, manifest=manifest)
        if not page_val["is_valid"]:
            errors.append(page_val["error"])

    return {
        "is_valid": len(errors) == 0,
        "errors": errors,
        "paper_id": str(paper_id) if paper_id else None,
        "page": page,
    }


def validate_report_citations(report_text: str, manifest: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, Any]:
    """
    Extract and validate all citations from a Markdown report.
    Returns audit statistics and any flagged citation anomalies.
    """
    papers = manifest if manifest is not None else load_manifest()
    pattern = re.compile(r"\b([A-Z]{2,4}\d{2})\s*,\s*p(?:p)?\.\s*(\d+)", re.IGNORECASE)
    matches = pattern.findall(report_text)

    citations = []
    invalid_count = 0

    for match in matches:
        pid = match[0].upper()
        pg = int(match[1])
        res = validate_source_page(pid, pg, manifest=papers)
        citation_info = {
            "citation": f"{pid}, p. {pg}",
            "paper_id": pid,
            "page": pg,
            "is_valid": res["is_valid"],
            "error": res["error"],
        }
        citations.append(citation_info)
        if not res["is_valid"]:
            invalid_count += 1

    return {
        "total_citations": len(citations),
        "valid_citations": len(citations) - invalid_count,
        "invalid_citations": invalid_count,
        "is_valid": invalid_count == 0,
        "citations": citations,
    }


def verify_quote_groundedness(paper_id: str, page: int, quote: str) -> Dict[str, Any]:
    """
    Verify whether an evidence quote exists on the given paper page in the indexed corpus chunks.
    """
    if not CHUNKS_PATH.exists():
        return {
            "is_grounded": False,
            "error": f"Chunks file not found at {CHUNKS_PATH}",
        }

    norm_quote = re.sub(r"\s+", " ", quote.strip().lower())
    norm_id = str(paper_id).strip().upper()

    with CHUNKS_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            chunk = json.loads(line)
            if chunk.get("paper_id") == norm_id and int(chunk.get("page", 0)) == int(page):
                chunk_text = re.sub(r"\s+", " ", chunk.get("text", "").lower())
                # Check for direct inclusion or high overlap
                if norm_quote in chunk_text:
                    return {
                        "is_grounded": True,
                        "paper_id": norm_id,
                        "page": int(page),
                        "match_type": "exact_substring",
                        "error": None,
                    }
                # Check key token containment if quote has formatting discrepancies
                quote_words = set(re.findall(r"\w{4,}", norm_quote))
                chunk_words = set(re.findall(r"\w{4,}", chunk_text))
                overlap = quote_words & chunk_words
                if len(quote_words) > 0 and len(overlap) / len(quote_words) >= 0.85:
                    return {
                        "is_grounded": True,
                        "paper_id": norm_id,
                        "page": int(page),
                        "match_type": "token_overlap_85+",
                        "error": None,
                    }

    return {
        "is_grounded": False,
        "paper_id": norm_id,
        "page": int(page),
        "error": f"Quote not found on page {page} of paper {norm_id}",
    }
