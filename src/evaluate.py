"""Retrieval evaluation for Neuro Literature Research Copilot."""

import argparse
import io
import json
import statistics
import time
from contextlib import redirect_stdout
from pathlib import Path

from src import research


DATA_DIR = Path("data")
OUTPUT_DIR = Path("outputs")


def load_jsonl(path):
    """Read a JSONL file and return its records."""
    records = []

    with path.open(encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                records.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON in {path}, line {line_number}: {exc}"
                ) from exc

    return records


def page_key(item):
    """Return a normalized paper/page identity."""
    try:
        page = int(item["page"])
    except (KeyError, TypeError, ValueError):
        return None

    paper_id = item.get("paper_id")

    if not paper_id or page < 1:
        return None

    return str(paper_id), page


def score_retrieval(retrieved, required_evidence, k=5):
    """
    Calculate page-level retrieval metrics.

    A retrieval hit requires both paper_id and PDF page to match
    an annotated gold evidence location.
    """
    if k < 1:
        raise ValueError("k must be at least 1.")

    gold_pages = {
        key
        for item in required_evidence
        if (key := page_key(item)) is not None
    }

    retrieved_pages = []
    seen = set()

    for item in retrieved[:k]:
        key = page_key(item)

        if key is not None and key not in seen:
            retrieved_pages.append(key)
            seen.add(key)

    matched_pages = set(retrieved_pages) & gold_pages

    first_relevant_rank = None

    for rank, item in enumerate(retrieved[:k], start=1):
        if page_key(item) in gold_pages:
            first_relevant_rank = rank
            break

    recall = (
        len(matched_pages) / len(gold_pages)
        if gold_pages else 0.0
    )

    precision = len(matched_pages) / k

    reciprocal_rank = (
        1.0 / first_relevant_rank
        if first_relevant_rank else 0.0
    )

    return {
        "gold_pages_count": len(gold_pages),
        "retrieved_unique_pages": len(retrieved_pages),
        "matched_pages_count": len(matched_pages),
        "matched_pages": [
            {"paper_id": p, "page": page}
            for p, page in sorted(matched_pages)
        ],
        "recall_at_k": recall,
        "source_page_precision_at_k": precision,
        "reciprocal_rank": reciprocal_rank,
        "first_relevant_rank": first_relevant_rank,
        "covered": bool(matched_pages),
    }


def evaluate(split="test", k=5, condition=None):
    """Evaluate the retrieval pipeline on the selected dataset split."""
    questions_path = DATA_DIR / "evaluation_questions.jsonl"
    labels_path = DATA_DIR / "evaluation_gold_labels.jsonl"

    if not questions_path.exists():
        raise FileNotFoundError(questions_path)

    if not labels_path.exists():
        raise FileNotFoundError(labels_path)

    questions = load_jsonl(questions_path)
    labels = load_jsonl(labels_path)

    question_by_id = {q["question_id"]: q for q in questions}
    label_by_id = {g["question_id"]: g for g in labels}

    if len(question_by_id) != len(questions):
        raise ValueError("Duplicate question IDs found.")

    if len(label_by_id) != len(labels):
        raise ValueError("Duplicate gold-label IDs found.")

    common_ids = sorted(set(question_by_id) & set(label_by_id))

    evaluated = []
    skipped = []

    for question_id in common_ids:
        question_record = question_by_id[question_id]
        gold = label_by_id[question_id]

        if split != "all" and question_record.get("split") != split:
            continue

        targets = question_record.get("target_conditions", [])
        target_condition = targets[0] if targets else None

        if condition and target_condition != condition:
            continue

        if gold.get("expected_status") == "pending_annotation":
            skipped.append({
                "question_id": question_id,
                "reason": "Gold annotation is pending.",
            })
            continue

        if not gold.get("required_evidence"):
            skipped.append({
                "question_id": question_id,
                "reason": "No required evidence is annotated.",
            })
            continue

        start = time.perf_counter()

        # Suppress the existing retriever's verbose passage printing.
        with redirect_stdout(io.StringIO()):
            retrieved = research.prepare_evidence(
                question=question_record["question"],
                top_k=k,
                condition=target_condition,
            )

        elapsed = time.perf_counter() - start

        metrics = score_retrieval(
            retrieved=retrieved,
            required_evidence=gold["required_evidence"],
            k=k,
        )

        evaluated.append({
            "question_id": question_id,
            "question": question_record["question"],
            "condition": target_condition,
            "split": question_record.get("split"),
            "expected_status": gold.get("expected_status"),
            "retrieved_count": len(retrieved),
            "elapsed_seconds": round(elapsed, 3),
            "metrics": metrics,
            "retrieved_evidence": [
                {
                    "rank": item.get("rank"),
                    "paper_id": item.get("paper_id"),
                    "page": item.get("page"),
                    "chunk_id": item.get("chunk_id"),
                    "cosine_distance": item.get("cosine_distance"),
                    "passage_excerpt": item.get("passage", "")[:300],
                }
                for item in retrieved
            ],
        })

        print(
            f"{question_id} | "
            f"Recall@{k}: {metrics['recall_at_k']:.3f} | "
            f"MRR: {metrics['reciprocal_rank']:.3f} | "
            f"Page precision@{k}: "
            f"{metrics['source_page_precision_at_k']:.3f}"
        )

    if not evaluated:
        raise RuntimeError(
            "No questions were evaluated. Check the split, condition, "
            "and gold-label annotations."
        )

    summary = {
        "split": split,
        "condition_filter": condition,
        "k": k,
        "questions_evaluated": len(evaluated),
        "questions_skipped": len(skipped),
        "mean_recall_at_k": statistics.mean(
            x["metrics"]["recall_at_k"] for x in evaluated
        ),
        "mean_mrr": statistics.mean(
            x["metrics"]["reciprocal_rank"] for x in evaluated
        ),
        "mean_source_page_precision_at_k": statistics.mean(
            x["metrics"]["source_page_precision_at_k"]
            for x in evaluated
        ),
        "question_coverage_at_k": statistics.mean(
            float(x["metrics"]["covered"]) for x in evaluated
        ),
        "mean_retrieval_seconds": statistics.mean(
            x["elapsed_seconds"] for x in evaluated
        ),
    }

    result = {
        "evaluation_type": "page_level_retrieval",
        "summary": summary,
        "results": evaluated,
        "skipped_questions": skipped,
        "limitations": [
            "Metrics evaluate retrieval of annotated paper/page locations.",
            "A page match does not prove that the retrieved passage supports "
            "the scientific claim.",
            "Citation correctness at the generated-claim level is not "
            "measured by this retrieval-only evaluation.",
            "The four-question test split is too small for strong statistical "
            "conclusions.",
            "Gold annotations still require human verification against "
            "the original PDFs."
        ],
    }

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    suffix = f"{split}_k{k}"
    if condition:
        suffix += f"_{condition}"

    json_path = OUTPUT_DIR / f"evaluation_{suffix}.json"
    markdown_path = OUTPUT_DIR / f"evaluation_{suffix}.md"

    with json_path.open("w", encoding="utf-8") as file:
        json.dump(result, file, indent=2, ensure_ascii=False)

    lines = [
        "# Neuro Literature Research Copilot — Evaluation",
        "",
        f"**Evaluation type:** {result['evaluation_type']}",
        f"**Split:** {split}",
        f"**Condition filter:** {condition or 'All conditions'}",
        f"**K:** {k}",
        f"**Questions evaluated:** {len(evaluated)}",
        f"**Questions skipped:** {len(skipped)}",
        "",
        "## Aggregate retrieval metrics",
        "",
        "| Metric | Score |",
        "|---|---:|",
        f"| Recall@{k} | {summary['mean_recall_at_k']:.4f} |",
        f"| MRR | {summary['mean_mrr']:.4f} |",
        (
            f"| Source-page precision@{k} | "
            f"{summary['mean_source_page_precision_at_k']:.4f} |"
        ),
        (
            f"| Question coverage@{k} | "
            f"{summary['question_coverage_at_k']:.4f} |"
        ),
        (
            f"| Mean retrieval time (seconds) | "
            f"{summary['mean_retrieval_seconds']:.3f} |"
        ),
        "",
        "## Per-question results",
        "",
        "| Question | Recall | MRR | Page precision |",
        "|---|---:|---:|---:|",
    ]

    for item in evaluated:
        m = item["metrics"]
        lines.append(
            f"| {item['question_id']} "
            f"| {m['recall_at_k']:.3f} "
            f"| {m['reciprocal_rank']:.3f} "
            f"| {m['source_page_precision_at_k']:.3f} |"
        )

    lines.extend([
        "",
        "## Limitations",
        "",
    ])

    lines.extend(f"- {item}" for item in result["limitations"])

    markdown_path.write_text("\n".join(lines), encoding="utf-8")

    print("\n===== EVALUATION SUMMARY =====")
    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\nJSON report:", json_path)
    print("Markdown report:", markdown_path)

    return result


def main():
    parser = argparse.ArgumentParser(
        description="Evaluate retrieval against annotated gold evidence."
    )

    parser.add_argument(
        "--split",
        choices=["development", "test", "all"],
        default="test",
    )
    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
    )
    parser.add_argument(
        "--condition",
        choices=[
            "alzheimers",
            "epilepsy",
            "parkinsons",
            "schizophrenia",
        ],
        default=None,
    )

    args = parser.parse_args()

    if not 1 <= args.top_k <= 20:
        parser.error("--top-k must be between 1 and 20.")

    evaluate(
        split=args.split,
        k=args.top_k,
        condition=args.condition,
    )


if __name__ == "__main__":
    main()
