"""Unit tests for citation and source-page validation."""

import unittest
from src.validation import (
    validate_citation_format,
    validate_source_page,
    validate_evidence_item,
    validate_report_citations,
    verify_quote_groundedness,
)


class TestCitationValidation(unittest.TestCase):

    def setUp(self):
        self.mock_manifest = {
            "ALZ01": {"paper_id": "ALZ01", "page_count": 5},
            "ALZ06": {"paper_id": "ALZ06", "page_count": 46},
            "EPI03": {"paper_id": "EPI03", "page_count": 12},
            "PAR07": {"paper_id": "PAR07", "page_count": 8},
            "SCH04": {"paper_id": "SCH04", "page_count": 5},
        }

    # 1. Citation string format tests
    def test_valid_single_page_citation(self):
        result = validate_citation_format("ALZ01, p. 4")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["paper_id"], "ALZ01")
        self.assertEqual(result["page"], 4)

    def test_valid_page_range_citation(self):
        result = validate_citation_format("PAR07, pp. 2-4")
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["paper_id"], "PAR07")
        self.assertEqual(result["page"], [2, 3, 4])

    def test_invalid_citation_format(self):
        bad_strings = ["ALZ01", "page 4", "Unknown, p. ?", "", None]
        for bad in bad_strings:
            res = validate_citation_format(bad)
            self.assertFalse(res["is_valid"], f"Should reject: {bad}")

    def test_inverted_page_range_rejected(self):
        result = validate_citation_format("PAR07, pp. 5-2")
        self.assertFalse(result["is_valid"])
        self.assertIn("Invalid page range", result["error"])

    # 2. Source-page boundaries and paper existence
    def test_valid_paper_and_in_bounds_page(self):
        result = validate_source_page("ALZ01", 3, manifest=self.mock_manifest)
        self.assertTrue(result["is_valid"])
        self.assertIsNone(result["error"])

    def test_unknown_paper_id_rejected(self):
        result = validate_source_page("FAKE99", 1, manifest=self.mock_manifest)
        self.assertFalse(result["is_valid"])
        self.assertIn("not found in manifest", result["error"])

    def test_out_of_bounds_page_rejected(self):
        # ALZ01 has 5 pages; page 9 is invalid
        result = validate_source_page("ALZ01", 9, manifest=self.mock_manifest)
        self.assertFalse(result["is_valid"])
        self.assertIn("exceeds max page count", result["error"])

    def test_zero_or_negative_page_rejected(self):
        for bad_page in [0, -2]:
            result = validate_source_page("ALZ01", bad_page, manifest=self.mock_manifest)
            self.assertFalse(result["is_valid"])
            self.assertIn("must be >= 1", result["error"])

    # 3. Evidence dictionary structure validation
    def test_validate_evidence_item_valid(self):
        item = {
            "paper_id": "ALZ01",
            "page": 2,
            "passage": "In this work, we propose a multi-modality AD classifier.",
        }
        result = validate_evidence_item(item, manifest=self.mock_manifest)
        self.assertTrue(result["is_valid"])
        self.assertEqual(len(result["errors"]), 0)

    def test_validate_evidence_item_missing_fields(self):
        item = {"passage": "Missing paper_id and page"}
        result = validate_evidence_item(item, manifest=self.mock_manifest)
        self.assertFalse(result["is_valid"])
        self.assertTrue(any("Missing 'paper_id'" in err for err in result["errors"]))
        self.assertTrue(any("Missing 'page'" in err for err in result["errors"]))

    # 4. Report citation scanning
    def test_validate_report_citations_all_valid(self):
        report = (
            "# Report\n"
            "Key findings in ALZ01, p. 2 and ALZ06, p. 5 confirm hippocampal atrophy.\n"
            "See also PAR07, p. 4 for SPECT findings."
        )
        result = validate_report_citations(report, manifest=self.mock_manifest)
        self.assertTrue(result["is_valid"])
        self.assertEqual(result["total_citations"], 3)
        self.assertEqual(result["invalid_citations"], 0)

    def test_validate_report_citations_flags_invalid(self):
        report = (
            "# Report\n"
            "Valid citation: ALZ01, p. 2.\n"
            "Hallucinated citation: FAKE99, p. 1.\n"
            "Out of bounds citation: ALZ01, p. 99.\n"
        )
        result = validate_report_citations(report, manifest=self.mock_manifest)
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["total_citations"], 3)
        self.assertEqual(result["valid_citations"], 1)
        self.assertEqual(result["invalid_citations"], 2)

    # 5. Text groundedness verification
    def test_verify_quote_groundedness_exact(self):
        quote = "Diagnosis of Alzheimer's Disease via Multi-modality 3D Convolutional Neural Network"
        result = verify_quote_groundedness("ALZ01", 1, quote)
        self.assertTrue(result["is_grounded"])

    def test_verify_quote_groundedness_mismatch(self):
        quote = "This arbitrary text definitely does not exist on page 1 of ALZ01"
        result = verify_quote_groundedness("ALZ01", 1, quote)
        self.assertFalse(result["is_grounded"])


if __name__ == "__main__":
    unittest.main()
