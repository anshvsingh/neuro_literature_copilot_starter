# Neuro Literature Research Copilot — Evaluation

**Evaluation type:** page_level_retrieval
**Split:** test
**Condition filter:** All conditions
**K:** 5
**Questions evaluated:** 4
**Questions skipped:** 0

## Aggregate retrieval metrics

| Metric | Score |
|---|---:|
| Recall@5 | 0.7500 |
| MRR | 0.6458 |
| Source-page precision@5 | 0.2000 |
| Question coverage@5 | 1.0000 |
| Mean retrieval time (seconds) | 6.660 |

## Per-question results

| Question | Recall | MRR | Page precision |
|---|---:|---:|---:|
| ADQ03 | 1.000 | 0.250 | 0.200 |
| EPQ03 | 1.000 | 1.000 | 0.200 |
| PDQ03 | 0.500 | 1.000 | 0.200 |
| SCQ03 | 0.500 | 0.333 | 0.200 |

## Limitations

- Metrics evaluate retrieval of annotated paper/page locations.
- A page match does not prove that the retrieved passage supports the scientific claim.
- Citation correctness at the generated-claim level is not measured by this retrieval-only evaluation.
- The four-question test split is too small for strong statistical conclusions.
- Gold annotations still require human verification against the original PDFs.