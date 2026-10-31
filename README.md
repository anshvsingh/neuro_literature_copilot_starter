# Neuro Literature Research Copilot

A Python-based research assistant that retrieves and organizes evidence from neuroscience research papers across four conditions: Alzheimer's disease, epilepsy, Parkinson's disease, and schizophrenia.

## Features

- PDF text extraction and chunking using PyMuPDF.
- Semantic retrieval using Sentence Transformers and ChromaDB.
- Condition-specific paper retrieval.
- Multi-round evidence retrieval with targeted follow-up searches.
- Rule-based evidence filtering and deduplication.
- Markdown research reports and structured JSON evidence.
- Retrieval evaluation using manually annotated paper/page references.
- Unit tests for evidence filtering and evaluation metrics.

## Workflow

1. Add research PDFs to the local data folders.
2. Run ingestion to extract text and build the ChromaDB index.
3. Submit a research question with an optional condition filter.
4. Retrieve relevant passages through semantic search.
5. Run targeted follow-up searches when required.
6. Filter and organize evidence into research reports.
7. Evaluate retrieval against manually annotated references.

**Note:** The current planner and synthesis are deterministic and rule-based, not LLM-powered. This project is a research-navigation prototype, not a validated clinical tool.

## Project Structure

```text
neuro_literature_copilot_starter/
├── data/
│   ├── papers/                 # Local PDFs (not committed)
│   ├── evaluation_questions.jsonl
│   ├── evaluation_gold_labels.jsonl
│   ├── gold_labels_template.jsonl
│   ├── questions_template.jsonl
│   └── manifest_template.csv
├── outputs/                    # Generated reports (not committed)
├── src/
│   ├── ingest.py
│   ├── retrieve.py
│   ├── research.py
│   ├── agentic_research.py
│   ├── evaluate.py
│   ├── extract_claims.py
│   ├── evidence_matrix.py
│   ├── paper_evidence_matrix.py
│   ├── classify_claim_origins.py
│   └── build_review_queue.py
├── tests/
│   ├── test_research_filter.py
│   └── test_evaluate.py
├── requirements.txt
└── README.md