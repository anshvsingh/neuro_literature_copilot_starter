import unittest

from src.evaluate import score_retrieval


class TestRetrievalMetrics(unittest.TestCase):

    def setUp(self):
        self.gold = [
            {"paper_id": "P1", "page": 3, "quote": "Evidence A"},
            {"paper_id": "P2", "page": 8, "quote": "Evidence B"},
        ]

    def test_all_gold_pages_retrieved(self):
        retrieved = [
            {"paper_id": "P1", "page": 3},
            {"paper_id": "P2", "page": 8},
        ]

        result = score_retrieval(retrieved, self.gold, k=5)

        self.assertEqual(result["recall_at_k"], 1.0)
        self.assertEqual(result["reciprocal_rank"], 1.0)
        self.assertEqual(result["matched_pages_count"], 2)

    def test_first_relevant_result_is_rank_two(self):
        retrieved = [
            {"paper_id": "P3", "page": 1},
            {"paper_id": "P1", "page": 3},
            {"paper_id": "P2", "page": 8},
        ]

        result = score_retrieval(retrieved, self.gold, k=5)

        self.assertEqual(result["recall_at_k"], 1.0)
        self.assertEqual(result["reciprocal_rank"], 0.5)

    def test_no_gold_evidence_retrieved(self):
        retrieved = [
            {"paper_id": "P3", "page": 1},
            {"paper_id": "P4", "page": 2},
        ]

        result = score_retrieval(retrieved, self.gold, k=5)

        self.assertEqual(result["recall_at_k"], 0.0)
        self.assertEqual(result["reciprocal_rank"], 0.0)
        self.assertFalse(result["covered"])

    def test_duplicate_page_does_not_inflate_recall(self):
        retrieved = [
            {"paper_id": "P1", "page": 3},
            {"paper_id": "P1", "page": 3},
            {"paper_id": "P1", "page": 3},
        ]

        result = score_retrieval(retrieved, self.gold, k=5)

        self.assertEqual(result["matched_pages_count"], 1)
        self.assertEqual(result["recall_at_k"], 0.5)

    def test_invalid_k_is_rejected(self):
        with self.assertRaises(ValueError):
            score_retrieval([], self.gold, k=0)


if __name__ == "__main__":
    unittest.main()
