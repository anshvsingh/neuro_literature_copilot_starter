
import unittest

from src.research import assess_passage


class TestReferenceFilter(unittest.TestCase):

    def test_reference_heading_and_numbered_entries(self):
        passage = (
            "The model achieved good results. References "
            "1. Smith, J. MRI classification. Journal of Medicine "
            "20 (2020) 10-20. "
            "2. Jones, A. Image analysis. Research Journal "
            "12 (2021) 30-40."
        )
        result = assess_passage(passage)
        self.assertTrue(result["is_reference_heavy"])

    def test_numbered_references_without_heading(self):
        passage = (
            "21. Solana-Lavalle, G. Classification of MRI scans, "
            "International Journal of Medical Informatics 119 "
            "(2018) 75-87. "
            "22. Tremblay, C. Olfactory bulb analysis, "
            "NeuroImage Clinical 28 (2020) 102457. "
            "23. Sivaranjini, S. Deep learning diagnosis, "
            "Multimedia Tools 79 (2020) 15467."
        )
        result = assess_passage(passage)
        self.assertTrue(result["is_reference_heavy"])

    def test_reference_entries_with_url(self):
        passage = (
            "48. Long, D.; Wang, J.; Xu, X. MRI classification. "
            "PLOS ONE (2012). "
            "49. Available online: "
            "https://example.org/paper (accessed in 2021)."
        )
        result = assess_passage(passage)
        self.assertTrue(result["is_reference_heavy"])

    def test_normal_scientific_passage_is_kept(self):
        passage = (
            "Imaging modalities including MRI and SPECT have been "
            "investigated for Parkinson disease detection. "
            "AlexNet uses transfer learning to classify MRI images, "
            "while three-dimensional convolutional neural networks "
            "learn features from volumetric brain scans. "
            "Researchers also discuss data leakage and validation."
        )
        result = assess_passage(passage)
        self.assertFalse(result["is_reference_heavy"])

    def test_empty_passage_is_flagged(self):
        result = assess_passage("")
        self.assertTrue(result["is_reference_heavy"])


if __name__ == "__main__":
    unittest.main()
