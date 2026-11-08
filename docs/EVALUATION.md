# Evaluation Benchmark & Results

## Benchmark Design

The evaluation dataset assesses page-level retrieval accuracy against expert-verified ground truth annotations across four neurological conditions:
1. **Alzheimer's Disease (AD)**
2. **Epilepsy (EP)**
3. **Parkinson's Disease (PD)**
4. **Schizophrenia (SC)**

The dataset contains **16 evaluation questions** balanced across conditions and splits:
- **Development Split:** 8 questions (2 per condition)
- **Held-Out Test Split:** 8 questions (2 per condition)

Every gold label contains:
- `question_id`: Unique identifier (e.g., `ADQ01`, `EPQ03`)
- `reference_answer`: Concise, verified answer grounded in paper evidence
- `required_evidence`: List of `{paper_id, page, quote}` tuples verified against source PDFs
- `expected_status`: `"supported"` or `"partially_supported"`
- `annotator_notes`: Traceability verification details

---

## Evaluation Metrics (k = 5)

A retrieval hit requires **both the paper ID and physical PDF page** to match an annotated gold evidence location.

### Summary Metrics Across Splits

| Metric | Development Split (8 Qs) | Test Split (8 Qs) | Full Benchmark (16 Qs) |
|---|---|---|---|
| **Mean Recall@5** | **71.9%** | **93.8%** | **82.8%** |
| **Mean MRR (Reciprocal Rank)** | **0.563** | **0.771** | **0.667** |
| **Question Coverage@5** | **87.5%** (7/8) | **100.0%** (8/8) | **93.8%** (15/16) |
| **Source Page Precision@5** | **30.0%** | **22.5%** | **26.3%** |
| **Mean Latency per Query** | **0.88s** | **0.92s** | **0.50s** |

---

## Detailed Question-by-Question Results

### Development Split

| Question ID | Condition | Question Type | Recall@5 | MRR | Precision@5 | Status |
|---|---|---|---|---|---|---|
| **ADQ01** | Alzheimer's | Modalities & ML Models | 0.750 | 1.000 | 0.600 | Covered |
| **ADQ02** | Alzheimer's | Brain Regions & Biomarkers | 0.500 | 1.000 | 0.200 | Covered |
| **EPQ01** | Epilepsy | Modalities & Classifiers | 1.000 | 1.000 | 0.600 | Covered |
| **EPQ02** | Epilepsy | ML Limitations & Black-box | 1.000 | 0.500 | 0.200 | Covered |
| **PDQ01** | Parkinson's | Modalities & Architectures | 0.000 | 0.000 | 0.000 | Uncovered (Broad) |
| **PDQ02** | Parkinson's | Data Splitting & Leakage | 1.000 | 0.250 | 0.200 | Covered |
| **SCQ01** | Schizophrenia | Biomarkers & Features | 1.000 | 0.500 | 0.400 | Covered |
| **SCQ02** | Schizophrenia | Deep vs Handcrafted Models | 0.500 | 0.250 | 0.200 | Covered |

### Test Split (Held-Out)

| Question ID | Condition | Question Type | Recall@5 | MRR | Precision@5 | Status |
|---|---|---|---|---|---|---|
| **ADQ03** | Alzheimer's | Limitations & Future Work | 1.000 | 0.333 | 0.200 | Covered |
| **ADQ04** | Alzheimer's | Hippocampal Biomarker | 1.000 | 1.000 | 0.200 | Covered |
| **EPQ03** | Epilepsy | Future Research Directions | 1.000 | 0.500 | 0.200 | Covered |
| **EPQ04** | Epilepsy | Multidomain EEG Features | 1.000 | 1.000 | 0.200 | Covered |
| **PDQ03** | Parkinson's | Clinical Use Limitations | 0.500 | 1.000 | 0.200 | Covered |
| **PDQ04** | Parkinson's | Subtyping & Consensus Issues | 1.000 | 1.000 | 0.200 | Covered |
| **SCQ03** | Schizophrenia | Generalizability & Grad-CAM | 1.000 | 0.333 | 0.400 | Covered |
| **SCQ04** | Schizophrenia | Model Explainability Heatmaps | 1.000 | 1.000 | 0.200 | Covered |

---

## Analysis & Remaining Limitations

1. **PDQ01 Broad Query Challenge:**
   - PDQ01 asks broadly about modalities and models in Parkinson's disease. Multiple papers in the 25-paper corpus discuss Parkinson's imaging, and general survey chunks compete with specific deep architecture methodology pages.
2. **Deterministic Heuristics:**
   - Heuristic quality filters effectively remove bibliography, publisher banners, and scanner parameter boilerplate. However, edge-case passages that blend methodology with publisher information require full-text inspection.
3. **Fixed Embedding Model Scope:**
   - `all-MiniLM-L6-v2` offers strong efficiency (sub-second queries), but dense technical biomedical terms (e.g. `ConvKAN`, `123I-FP-CIT SPECT`) benefit from domain-specific biomedical models (e.g., PubMedBERT) in future iterations.
