import unittest

from src.answer import is_answerable_sentence, split_sentences


class TestSentenceSplitting(unittest.TestCase):

    def test_offsets_reproduce_exact_sentences(self):
        text = (
            "EEG remains an important diagnostic test for epilepsy. "
            "CNN models achieved 98% accuracy on the Bonn dataset. "
            "Future work should evaluate wearable devices."
        )
        spans = split_sentences(text)
        self.assertEqual(len(spans), 3)
        self.assertEqual(text[spans[1][0]:spans[1][1]],
                         "CNN models achieved 98% accuracy on the Bonn dataset.")

    def test_does_not_split_on_lowercase_after_period(self):
        text = "Results were reported by Smith et al. in their cohort study of patients."
        self.assertEqual(len(split_sentences(text)), 1)

    def test_unterminated_tail_is_kept(self):
        text = "First complete sentence about MRI biomarkers. Second sentence is cut off mid"
        spans = split_sentences(text)
        self.assertEqual(text[spans[-1][0]:spans[-1][1]], "Second sentence is cut off mid")


class TestAnswerableSentence(unittest.TestCase):

    def test_accepts_substantive_sentence(self):
        self.assertTrue(is_answerable_sentence(
            "Hippocampal atrophy measured on structural MRI is a widely used biomarker of Alzheimer's disease."
        ))

    def test_rejects_short_fragment(self):
        self.assertFalse(is_answerable_sentence("classification methods for seizure detection."))

    def test_rejects_disclosure_statement(self):
        self.assertFalse(is_answerable_sentence(
            "The author has received speaker honoraria from several pharmaceutical companies and journals."
        ))

    def test_rejects_citation_dense_line(self):
        self.assertFalse(is_answerable_sentence(
            "Prior studies [1], [2], [3], [4] used deep learning for classification of EEG signals here."
        ))

    def test_rejects_figure_caption(self):
        self.assertFalse(is_answerable_sentence(
            "FIGURE 3: The limitations of deep learning models when used for epileptic seizure detection."
        ))

    def test_rejects_title_line(self):
        self.assertFalse(is_answerable_sentence(
            "Epileptic Seizures Detection Using Deep Learning Techniques: A Review Afshin Shoeibi, Marjane Khodatars"
        ))


if __name__ == "__main__":
    unittest.main()
