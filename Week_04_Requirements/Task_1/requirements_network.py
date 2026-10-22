"""LangGraph requirements-refinement network.

The normal mode uses three OpenAI models.  ``--offline`` is intentionally
provided for deterministic smoke tests when an API key is unavailable; it is
not a replacement for the LLM refinement path.
"""

from __future__ import annotations

import argparse
import hashlib
import logging
import os
import re
from pathlib import Path
from typing import Any, Literal, TypedDict

from pydantic import BaseModel, Field


LOGGER = logging.getLogger("requirements_network")


Priority = Literal["must", "should", "could", "deferred"]


class Candidate(BaseModel):
    name: str
    statement: str
    explanation: str
    priority: Priority
    category: str = "General"
    sources: list[str] = Field(min_length=1)
    source_evidence: list[str] = Field(default_factory=list)


class CandidateBatch(BaseModel):
    candidates: list[Candidate]


class Review(BaseModel):
    approved: bool
    issues: list[str] = Field(default_factory=list)
    discarded: list[Candidate] = Field(default_factory=list)


class GraphState(TypedDict, total=False):
    documents: list[dict[str, str]]
    candidates: list[Candidate]
    review: Review
    requirements: list[Candidate]
    discarded: list[dict[str, str]]
    feedback: str
    attempts: int


def discover_documents(input_dir: Path) -> list[dict[str, str]]:
    """Read all supported text-like files below *input_dir* recursively."""
    LOGGER.info("Scanning input directory: %s", input_dir)
    if not input_dir.is_dir():
        raise FileNotFoundError(f"Input directory does not exist: {input_dir}")
    documents: list[dict[str, str]] = []
    for path in sorted(p for p in input_dir.rglob("*") if p.is_file()):
        if path.suffix.lower() not in {".txt", ".eml", ".md", ".csv", ".json"}:
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="replace").strip()
        except OSError as exc:
            raise OSError(f"Could not read input document {path}: {exc}") from exc
        if text:
            documents.append({"name": path.relative_to(input_dir).as_posix(), "text": text})
    if not documents:
        raise ValueError(f"No supported text documents found under {input_dir}")
    LOGGER.info("Loaded %d documents", len(documents))
    return documents


def load_documents(state: GraphState) -> GraphState:
    """Deterministic graph node: normalize and bound document payloads."""
    docs = state["documents"]
    LOGGER.info("Node load_documents: normalizing %d documents", len(docs))
    return {"documents": [{"name": d["name"], "text": d["text"].strip()} for d in docs]}


def _document_packet(documents: list[dict[str, str]]) -> str:
    return "\n\n".join(f"DOCUMENT: {d['name']}\n{d['text']}" for d in documents)


def _llm(model: str):
    LOGGER.debug("Creating OpenAI chat model: %s", model)
    try:
        from langchain_openai import ChatOpenAI
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "langchain-openai is not installed in the Python environment running this script. "
            "Activate the project virtual environment and run: "
            "python -m pip install -r Week_04_Requirements\\Task_1\\requirements.txt"
        ) from exc

    return ChatOpenAI(model=model, temperature=0)


def extract_candidates(state: GraphState) -> GraphState:
    """LLM node 1: extract atomic candidate requirements with provenance."""
    LOGGER.info("Node extract_candidates: extracting from %d documents", len(state["documents"]))
    prompt = """You are a requirements analyst. Extract every actionable software
requirement from the source corpus. Preserve uncertain or conflicting requests
as candidates rather than silently choosing. Split compound requirements into
atomic requirements. Do not invent behavior. Every candidate must cite one or
more exact source file names and include a short evidence quote.
Return only the requested structured schema.

SOURCE CORPUS:
"""
    try:
        batch = _llm("gpt-5-mini").with_structured_output(CandidateBatch).invoke(
            prompt + _document_packet(state["documents"])
        )
    except Exception:
        LOGGER.exception("Node extract_candidates failed")
        raise
    LOGGER.info("Node extract_candidates: produced %d candidates", len(batch.candidates))
    return {"candidates": batch.candidates, "attempts": 1}


def refine_candidates(state: GraphState) -> GraphState:
    """LLM node 2: merge duplicates and normalize requirement language."""
    feedback = state.get("feedback", "No previous review feedback.")
    LOGGER.info(
        "Node refine_candidates: refining %d candidates (attempt %d)",
        len(state["candidates"]),
        state.get("attempts", 1) + 1,
    )
    payload = CandidateBatch(candidates=state["candidates"]).model_dump_json()
    prompt = f"""You are a senior requirements editor. Normalize the candidates
below into a complete, non-duplicated set. Merge semantic duplicates while
unioning their source lists and evidence. Keep distinct requirements distinct.
Use consistent 'The system must/should...' language. Choose must for legal,
business-critical, safety, security, or explicitly mandatory behavior; should
for important expected behavior; could for optional enhancements; deferred for
unresolved requests. Keep paragraph-length explanations. Do not drop a
candidate merely because it conflicts: retain it for the validator to classify.
Review feedback from the previous pass: {feedback}
Return only the structured schema.

CANDIDATES:
{payload}"""
    try:
        batch = _llm("gpt-4o-mini").with_structured_output(CandidateBatch).invoke(prompt)
    except Exception:
        LOGGER.exception("Node refine_candidates failed")
        raise
    LOGGER.info("Node refine_candidates: produced %d candidates", len(batch.candidates))
    return {"candidates": batch.candidates, "attempts": state.get("attempts", 1) + 1}


def validate_candidates(state: GraphState) -> GraphState:
    """LLM node 3: check completeness, contradictions, and nonsensical items."""
    LOGGER.info(
        "Node validate_candidates: reviewing %d candidates (attempt %d)",
        len(state["candidates"]),
        state.get("attempts", 1),
    )
    payload = CandidateBatch(candidates=state["candidates"]).model_dump_json()
    prompt = f"""You are a strict requirements reviewer. Check this proposed
set for semantic duplicates, contradictions, unsupported inventions, missing
source provenance, non-atomic statements, and inconsistent priority language.
If a candidate is conflicting or nonsensical, put it in discarded with a
specific reason encoded in its explanation. Set approved true only when no
repairable issue remains. Do not discard a merely ambiguous requirement;
mark it deferred instead. Return only the structured schema.

PROPOSED REQUIREMENTS:
{payload}"""
    try:
        review = _llm("gpt-4.1-nano").with_structured_output(Review).invoke(prompt)
    except Exception:
        LOGGER.exception("Node validate_candidates failed")
        raise
    LOGGER.info(
        "Node validate_candidates: approved=%s, issues=%d, discarded=%d",
        review.approved,
        len(review.issues),
        len(review.discarded),
    )
    return {"review": review, "feedback": "; ".join(review.issues)}


def route_review(state: GraphState) -> str:
    review = state["review"]
    if review.approved or state.get("attempts", 1) >= 3:
        LOGGER.info("Feedback loop complete: routing to finalize")
        return "finalize"
    LOGGER.info("Feedback loop: routing back to refine_candidates")
    return "refine"


def finalize(state: GraphState) -> GraphState:
    """Deterministic graph node: stable IDs, exact deduplication, and output data."""
    LOGGER.info("Node finalize: deduplicating %d candidates", len(state["candidates"]))
    rejected_keys = {
        re.sub(r"\W+", " ", item.statement.lower()).strip()
        for item in state.get("review", Review(approved=True)).discarded
    }
    unique: dict[str, Candidate] = {}
    for candidate in state["candidates"]:
        key = re.sub(r"\W+", " ", candidate.statement.lower()).strip()
        if key in rejected_keys:
            continue
        if key not in unique:
            unique[key] = candidate
        else:
            prior = unique[key]
            unique[key] = prior.model_copy(
                update={
                    "sources": sorted(set(prior.sources + candidate.sources)),
                    "source_evidence": sorted(
                        set(prior.source_evidence + candidate.source_evidence)
                    ),
                }
            )
    requirements = sorted(unique.values(), key=lambda c: (c.category.lower(), c.name.lower()))
    discarded = [
        {"name": item.name, "reason": item.explanation, "sources": ", ".join(item.sources)}
        for item in state.get("review", Review(approved=True)).discarded
    ]
    LOGGER.info(
        "Node finalize: accepted=%d, discarded=%d",
        len(requirements),
        len(discarded),
    )
    return {"requirements": requirements, "discarded": discarded}


def build_graph():
    from langgraph.graph import END, START, StateGraph

    LOGGER.debug("Building LangGraph workflow")
    graph = StateGraph(GraphState)
    graph.add_node("load_documents", load_documents)
    graph.add_node("extract_candidates", extract_candidates)
    graph.add_node("refine_candidates", refine_candidates)
    graph.add_node("validate_candidates", validate_candidates)
    graph.add_node("finalize", finalize)
    graph.add_edge(START, "load_documents")
    graph.add_edge("load_documents", "extract_candidates")
    graph.add_edge("extract_candidates", "refine_candidates")
    graph.add_edge("refine_candidates", "validate_candidates")
    graph.add_conditional_edges("validate_candidates", route_review, {"refine": "refine_candidates", "finalize": "finalize"})
    graph.add_edge("finalize", END)
    compiled = graph.compile()
    LOGGER.debug("LangGraph workflow compiled successfully")
    return compiled


def _offline_candidates(documents: list[dict[str, str]]) -> list[Candidate]:
    """Conservative smoke-test extractor; it never claims to be LLM quality."""
    LOGGER.info("Offline mode: extracting candidates without OpenAI")
    candidates: list[Candidate] = []
    for doc in documents:
        for sentence in re.split(r"(?<=[.!?])\s+|\n+", doc["text"]):
            sentence = re.sub(r"\s+", " ", sentence).strip(" -")
            if len(sentence) < 30 or not re.search(r"\b(must|should|required|shall|need)\b", sentence, re.I):
                continue
            digest = hashlib.sha1(sentence.encode()).hexdigest()[:8]
            candidates.append(Candidate(
                name=f"Candidate {digest}",
                statement=f"The system should address: {sentence}",
                explanation=sentence,
                priority="should",
                sources=[doc["name"]],
                source_evidence=[sentence[:240]],
            ))
    LOGGER.info("Offline mode: produced %d candidates", len(candidates))
    return candidates


def render_markdown(requirements: list[Candidate], discarded: list[dict[str, str]], input_dir: Path) -> str:
    lines = [
        "# Software Requirements Specification", "",
        f"_Generated from `{input_dir}`._", "",
        "## Priority scale", "",
        "- **must**: Required for acceptance or a core/legal/business need.",
        "- **should**: Important and expected, but a temporary workaround exists.",
        "- **could**: Useful enhancement that can be postponed.",
        "- **deferred**: Identified need awaiting clarification or later scope.", "",
        "## Requirements", "",
    ]
    for number, req in enumerate(requirements, 1):
        lines += [
            f"### REQ-{number:03d}: {req.name}",
            f"**Priority:** `{req.priority}`  ",
            f"**Category:** {req.category}  ",
            f"**Derived from:** {', '.join(sorted(set(req.sources)))}", "",
            req.statement, "", f"**Explanation:** {req.explanation}", "",
        ]
    lines += ["## Discarded or unresolved candidates", ""]
    if discarded:
        for item in discarded:
            lines += [f"- **{item['name']}** ({item['sources']}): {item['reason']}"]
    else:
        lines.append("No candidates were discarded by the validator.")
    return "\n".join(lines) + "\n"


def run(input_dir: Path, output: Path, offline: bool = False) -> None:
    LOGGER.info("Starting requirements refinement (offline=%s)", offline)
    documents = discover_documents(input_dir)
    if offline:
        requirements = _offline_candidates(documents)
        discarded: list[dict[str, str]] = []
    else:
        if not os.getenv("OPENAI_API_KEY"):
            raise RuntimeError("OPENAI_API_KEY is required for LLM mode; use --offline only for smoke tests.")
        LOGGER.info("Invoking LangGraph workflow")
        result = build_graph().invoke({"documents": documents})
        requirements = result["requirements"]
        discarded = result["discarded"]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render_markdown(requirements, discarded, input_dir), encoding="utf-8")
    LOGGER.info("Wrote %d requirements to %s", len(requirements), output)
    print(f"Wrote {len(requirements)} requirements to {output}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--offline", action="store_true", help="Run deterministic smoke-test extraction without OpenAI.")
    parser.add_argument(
        "--log-level",
        choices=("DEBUG", "INFO", "WARNING", "ERROR"),
        default="INFO",
        help="Logging verbosity (default: INFO).",
    )
    args = parser.parse_args()
    logging.basicConfig(
        level=getattr(logging, args.log_level),
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    )
    run(args.input_dir, args.output, args.offline)


if __name__ == "__main__":
    main()
