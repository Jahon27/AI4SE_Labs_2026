# Task 1 — Requirements Refinement Using LangGraph

## 1. Task Description

The goal of this task was to create a multi-agent system that processes software requirements from different documents and generates one structured requirements specification.

The solution was implemented in Python using LangGraph and OpenAI models.

## 2. Implementation

The system uses three LLM agents and two deterministic nodes.

| Node | Model | Purpose |
|------|-------|---------|
| Load Documents | Deterministic | Reads input files |
| Extract Candidates | gpt-5-mini | Extracts requirements |
| Refine Candidates | gpt-4o-mini | Improves and merges requirements |
| Validate Candidates | gpt-4.1-nano | Checks requirements for problems |
| Finalize | Deterministic | Removes duplicates and prepares the output |

The agents work in the following order:

1. Input documents are loaded.
2. The first agent extracts possible requirements.
3. The second agent improves their descriptions and removes duplicates.
4. The third agent checks the requirements for errors and inconsistencies.
5. If problems are found, the requirements are sent back for refinement.
6. The final requirements are saved in a Markdown file.

## 3. Feedback Loop
The system includes a feedback loop between the refinement and validation agents.

If the validation agent finds problems, it sends feedback to the refinement agent. The refinement agent tries to fix these problems, and the requirements are checked again.

The number of attempts is limited to prevent an infinite loop.

## 4. Output
The provided output file contains 64 requirements for a library management and reporting system.

Each requirement includes:

- A unique ID (REQ-001, REQ-002, etc.).
- A name and description.
- A priority (must, should, could, or deferred).
- A category.
- References to source documents.
- An explanation of the requirement.

The output also contains a list of discarded requirements with reasons for their rejection.

The requirements cover library reporting, item transfers, capacity management, deletion auditing, patron information, and other functions.

## 5. Task Requirements

The implementation includes:

- Three LLM nodes using three different OpenAI models.
- Deterministic nodes for document processing and finalization.
- A feedback loop for improving requirements.
- LangGraph for connecting and controlling the nodes.
- A single Markdown output document.
- Requirement IDs, priorities, descriptions, and source references.
- Deduplication and validation steps.
- A list of discarded requirements.

## 6. Limitations

The system depends on LLM responses, so some requirements may be missed or interpreted incorrectly.

Processing can also take time because multiple API requests are needed.

The feedback loop has a maximum number of attempts, so not every issue is guaranteed to be fixed.

## 7. Conclusion
In this task, was implemented a multi-agent requirements refinement system
using Python, LangGraph, and three OpenAI models. The system can extract, refine, and validate requirements from input documents and prepare a structured Markdown specification. The result demonstrates how multiple AI agents can work together to automate part of the requirements engineering process.