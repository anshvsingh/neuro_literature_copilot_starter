"""
Lightweight adaptive research workflow for Neuro Literature Research Copilot.

This module reuses the existing retrieval, filtering, synthesis, and
report-generation functions. It does not modify retrieve.py or research.py.

The planner is deterministic and rule-based; it is not an LLM agent.
"""

import argparse
import json
import math
import re
from pathlib import Path

from src import research


CONDITION_LABELS = {
    "alzheimers": "Alzheimer's disease",
    "epilepsy": "epilepsy",
    "parkinsons": "Parkinson's disease",
    "schizophrenia": "schizophrenia",
}

METHOD_CUES = re.compile(
    r"\b("
    r"MRI|PET|SPECT|DaTscan|EEG|MEG|DTI|fMRI|"
    r"CNNs?|SVMs?|GCNs?|RNNs?|LSTMs?|"
    r"random forests?|DenseNet|AlexNet|"
    r"machine learning|deep learning|"
    r"biomarkers?|wavelet|spectral features?|"
    r"support vector machines?|classifiers?"
    r")\b|magnetic resonance|diffusion tensor imaging",
    re.IGNORECASE,
)

LIMITATION_CUES = re.compile(
    r"\b("
    r"limitations?|future work|future research|"
    r"generaliz\w*|validation|cross-validation|"
    r"data leakage|overfitting|overfitted|"
    r"bias|clinical practice|routine use|"
    r"dataset size|sample size|external testing|"
    r"independent test"
    r")\b",
    re.IGNORECASE,
)


def _condition_label(condition):
    """Return a readable condition name."""
    return CONDITION_LABELS.get(condition, "the selected research topic")


def _evidence_text(evidence):
    """Combine retrieved passages for simple evidence-coverage checks."""
    return " ".join(
        item.get("passage", "")
        for item in evidence
    )


def _evidence_key(item):
    """Create a stable key for deduplicating retrieved passages."""
    chunk_id = item.get("chunk_id")

    if chunk_id:
        return str(chunk_id)

    return "|".join(
        str(item.get(field, ""))
        for field in ("paper_id", "page", "passage")
    )


def _sort_distance(item):
    """Sort smaller cosine distances ahead of larger distances."""
    try:
        return float(item.get("cosine_distance", math.inf))
    except (TypeError, ValueError):
        return math.inf



def _is_low_context_table_fragment(passage):
    """
    Flag compact passages dominated by numbers and model labels.

    This is deliberately conservative. It flags passages for exclusion
    from the main report, while preserving their details in the JSON trace.
    """
    text = passage.strip()

    if not text or len(text) > 700:
        return False

    numbers = re.findall(
        r"(?<![A-Za-z])[-+]?\d+(?:\.\d+)?%?",
        text,
    )

    model_labels = set(re.findall(
        r"\b(?:CNN|GCN|SVM|ConvKAN|ConvKA|DenseNet|AlexNet)\b",
        text,
        re.IGNORECASE,
    ))

    words = re.findall(r"\b[\w.-]+\b", text)
    numeric_ratio = len(numbers) / max(1, len(words))

    sentence_starts = len(re.findall(
        r"[.!?]\s+[A-Z]",
        text,
    ))

    return (
        len(numbers) >= 8
        and len(model_labels) >= 2
        and numeric_ratio >= 0.20
        and sentence_starts <= 2
    )


def run_research(question, condition=None, top_k=5, name=None):
    """
    Run adaptive retrieval, combine evidence, and generate a report.

    Workflow:
      1. Retrieve evidence for the original question.
      2. Check for method/modality evidence.
      3. Search for methods if coverage appears weak.
      4. Check for limitation/validation evidence.
      5. Search for limitations if coverage appears weak.
      6. Deduplicate and rank the combined evidence.
      7. Generate the existing research report and save the trace.

    top_k is the maximum number of passages retrieved per round.
    The final report retains up to 2 * top_k unique passages.
    """

    question = question.strip()

    if not question:
        raise ValueError("Research question cannot be empty.")

    if top_k < 1 or top_k > 20:
        raise ValueError("top_k must be between 1 and 20.")

    if condition and condition not in CONDITION_LABELS:
        raise ValueError(
            f"Unsupported condition: {condition}. "
            f"Choose from: {', '.join(CONDITION_LABELS)}"
        )

    subject = _condition_label(condition)

    evidence_by_key = {}
    retrieval_trace = []
    rejected_evidence = []

    def retrieve_round(round_id, purpose, query):
        """Retrieve one round and merge its passages with existing evidence."""
        print("\n" + "=" * 75)
        print(f"RESEARCH ROUND: {round_id}")
        print(f"Purpose: {purpose}")
        print(f"Query: {query}")
        print("=" * 75)

        results = research.prepare_evidence(
            question=query,
            top_k=top_k,
            condition=condition,
        )

        added = 0

        for item in results:
            record = dict(item)

            # Reject compact numerical fragments from the main report.
            # Preserve their identity and reason in the workflow trace.
            if _is_low_context_table_fragment(
                record.get("passage", "")
            ):
                rejected_evidence.append({
                    "round_id": round_id,
                    "paper_id": record.get("paper_id"),
                    "page": record.get("page"),
                    "chunk_id": record.get("chunk_id"),
                    "reason": (
                        "Possible low-context numerical table fragment; "
                        "manual inspection required."
                    ),
                    "passage_excerpt": record.get("passage", "")[:500],
                })
                continue

            key = _evidence_key(record)

            if key not in evidence_by_key:
                record["retrieved_by"] = [round_id]
                record["retrieval_queries"] = [query]
                record["retrieval_round_ranks"] = {
                    round_id: item.get("rank", 999)
                }
                record["first_retrieval_rank"] = item.get("rank", 999)
                evidence_by_key[key] = record
                added += 1
            else:
                existing = evidence_by_key[key]

                if round_id not in existing["retrieved_by"]:
                    existing["retrieved_by"].append(round_id)

                existing["retrieval_round_ranks"][round_id] = (
                    item.get("rank", 999)
                )

                if query not in existing["retrieval_queries"]:
                    existing["retrieval_queries"].append(query)

        round_record = {
            "round_id": round_id,
            "purpose": purpose,
            "query": query,
            "passages_returned": len(results),
            "new_unique_passages": added,
            "total_unique_passages": len(evidence_by_key),
        }

        retrieval_trace.append(round_record)

        print("\nRound summary:")
        print("Passages returned:", len(results))
        print("New unique passages:", added)
        print("Total unique passages:", len(evidence_by_key))

        return added

    # Round 1: Always begin with the original research question.
    retrieve_round(
        round_id="R1",
        purpose="Original research question",
        query=question,
    )

    current_evidence = list(evidence_by_key.values())
    current_text = _evidence_text(current_evidence)

    # Plan follow-up searches from the requested aspects of the question.
    # Explicitly requested aspects are searched even when broad keywords
    # happened to appear in the first set of retrieved passages.

    method_requested = bool(re.search(
        r"\b(imaging|modalit\w*|biomarker\w*|feature\w*|"
        r"machine.learning|deep.learning|model\w*|algorithm\w*|"
        r"classifier\w*|method\w*|diagnostic|detection|prediction)\b",
        question,
        re.IGNORECASE,
    ))

    limitation_requested = bool(re.search(
        r"\b(limitation\w*|challenge\w*|validation|generaliz\w*|"
        r"clinical|bias|leakage|overfitting|future research|"
        r"future work|weakness\w*)\b",
        question,
        re.IGNORECASE,
    ))

    # Broad questions without explicit aspects receive both follow-ups.
    if not method_requested and not limitation_requested:
        method_requested = True
        limitation_requested = True

    if method_requested:
        method_query = (
            f"Which imaging modalities, biomarkers, signal features, "
            f"datasets, and machine-learning or deep-learning models "
            f"are reported for {subject}? "
            f"Research question: {question}"
        )

        print(
            "\nPlanner decision: the question requests methods or "
            "modalities. Running a targeted search."
        )
        retrieve_round(
            round_id="R2",
            purpose="Targeted methods and modalities search",
            query=method_query,
        )
    else:
        print("\nPlanner decision: methods follow-up not requested.")

    if limitation_requested:
        limitation_query = (
            f"What limitations, validation problems, data leakage risks, "
            f"dataset biases, generalizability concerns, clinical "
            f"translation issues, and future research directions are "
            f"reported for {subject}? "
            f"Research question: {question}"
        )

        print(
            "\nPlanner decision: the question requests limitations "
            "or challenges. Running a targeted search."
        )
        retrieve_round(
            round_id="R3",
            purpose="Targeted limitations and validation search",
            query=limitation_query,
        )
    else:
        print("\nPlanner decision: limitations follow-up not requested.")

    # Rank the combined evidence by its best retrieval distance.
    combined_evidence = sorted(
        evidence_by_key.values(),
        key=lambda item: (
            -len(item.get("retrieved_by", [])),
            item.get("first_retrieval_rank", 999),
            _sort_distance(item),
        ),
    )

    max_final_evidence = top_k * 2
    selected_evidence = combined_evidence[:max_final_evidence]

    for rank, item in enumerate(selected_evidence, start=1):
        item["rank"] = rank

    distinct_papers = sorted({
        item.get("paper_id", "Unknown")
        for item in selected_evidence
    })

    final_text = _evidence_text(selected_evidence)

    workflow = {
        "workflow_type": "lightweight_adaptive_retrieval",
        "planner_type": "deterministic_rule_based_coverage_checks",
        "original_question": question,
        "condition": condition,
        "top_k_per_round": top_k,
        "max_final_evidence": max_final_evidence,
        "retrieval_rounds": retrieval_trace,
        "quality_rejection_count": len(rejected_evidence),
        "rejected_evidence": rejected_evidence,
        "total_unique_passages": len(combined_evidence),
        "selected_passages": len(selected_evidence),
        "distinct_papers": distinct_papers,
        "method_evidence_detected": bool(
            METHOD_CUES.search(final_text)
        ),
        "limitation_evidence_detected": bool(
            LIMITATION_CUES.search(final_text)
        ),
        "planner_limitation": (
            "Coverage checks use keyword rules. They do not prove "
            "that evidence is complete or scientifically correct."
        ),
        "synthesis_method": (
            "Existing rule-based synthesis in src.research"
        ),
    }

    # Reuse the existing report and evidence JSON generator.
    output_name = name or f"agentic_{condition or 'all'}"

    report_path, evidence_path = research.save_outputs(
        question=question,
        evidence=selected_evidence,
        condition=condition,
        name=output_name,
    )

    # Add the adaptive workflow trace to the saved evidence JSON.
    with Path(evidence_path).open(encoding="utf-8") as f:
        evidence_data = json.load(f)

    evidence_data["agentic_workflow"] = workflow

    with Path(evidence_path).open("w", encoding="utf-8") as f:
        json.dump(
            evidence_data,
            f,
            indent=4,
            ensure_ascii=False,
            default=str,
        )

    # Add a readable planning section to the Markdown report.
    report_text = Path(report_path).read_text(encoding="utf-8")

    trace_lines = [
        "## Adaptive research planning and retrieval",
        "",
        (
            "The workflow first searched the original question and then "
            "used keyword-based coverage checks to decide whether "
            "additional searches were needed."
        ),
        "",
        "**Planner:** deterministic rule-based coverage checks",
        "",
        "**Retrieval rounds:**",
        "",
    ]

    for round_info in retrieval_trace:
        trace_lines.extend([
            (
                f"- **{round_info['round_id']} — "
                f"{round_info['purpose']}:** "
                f"{round_info['passages_returned']} passages returned; "
                f"{round_info['new_unique_passages']} new unique passages."
            ),
            f"  - Query: {round_info['query']}",
        ])

    trace_lines.extend([
        "",
        f"- **Unique passages collected:** {len(combined_evidence)}",
        f"- **Passages included in report:** {len(selected_evidence)}",
        f"- **Distinct paper IDs:** {len(distinct_papers)}",
        "",
        (
            "**Important:** The planner uses keyword-based coverage "
            "checks. Retrieved passages and generated synthesis still "
            "require human verification."
        ),
        "",
    ])

    trace_section = "\n".join(trace_lines)

    if "## Summary" in report_text:
        report_text = report_text.replace(
            "## Summary",
            trace_section + "## Summary",
            1,
        )
    else:
        report_text += "\n\n" + trace_section

    Path(report_path).write_text(report_text, encoding="utf-8")

    print("\n" + "=" * 75)
    print("ADAPTIVE RESEARCH COMPLETED")
    print("=" * 75)
    print("Condition:", condition or "All conditions")
    print("Retrieval rounds:", len(retrieval_trace))
    print("Unique passages collected:", len(combined_evidence))
    print("Passages in final report:", len(selected_evidence))
    print("Distinct papers:", len(distinct_papers))
    print("\nMarkdown report:", report_path)
    print("Evidence JSON:", evidence_path)

    return report_path, evidence_path


def main():
    parser = argparse.ArgumentParser(
        description="Run the adaptive Neuro Literature Research Copilot."
    )

    parser.add_argument(
        "--question",
        required=True,
        help="Research question to investigate.",
    )

    parser.add_argument(
        "--condition",
        choices=list(CONDITION_LABELS),
        default=None,
        help="Optional condition filter.",
    )

    parser.add_argument(
        "--top-k",
        type=int,
        default=5,
        help="Passages to retrieve per round (1-20). Default: 5.",
    )

    parser.add_argument(
        "--name",
        default=None,
        help="Optional output filename prefix.",
    )

    args = parser.parse_args()

    run_research(
        question=args.question,
        condition=args.condition,
        top_k=args.top_k,
        name=args.name,
    )


if __name__ == "__main__":
    main()
