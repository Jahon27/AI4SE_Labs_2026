---
name: architecture-decision
description: 'Use when analyzing software requirements, proposing and comparing software architectures, selecting an architecture, or creating and reviewing an Architecture Decision Record (ADR). Guides evidence-based comparison of at least three options, trade-off analysis, decision making, and clear ADR documentation.'
argument-hint: 'Describe the project, requirements, constraints, or ADR to analyze'
user-invocable: true
disable-model-invocation: false
---

# Architecture Decision Workflow

## Purpose

Use this skill to turn software requirements into an explainable architecture
decision. The workflow is technology-neutral and applies to new systems,
existing-system changes, and ADR reviews.

The output should separate:

1. Facts stated by the requirements.
2. Assumptions made because requirements are incomplete.
3. Architecture consequences of those facts and assumptions.
4. The selected decision and the reasons for it.

Do not choose an architecture before understanding the requirements.

## When to use

- Analyze functional and non-functional requirements before design.
- Propose multiple architecture options.
- Compare modular monoliths, microservices, event-driven systems, layered
  systems, serverless systems, or other relevant styles.
- Select an architecture using explicit decision criteria.
- Create, improve, or review an ADR.
- Explain architecture trade-offs to a technical or non-technical audience.

## Procedure

### 1. Establish scope and evidence

1. Identify the system purpose, users, business capabilities, and boundaries.
2. Read the available requirements, existing architecture documents, and
   relevant code or repository conventions.
3. Record the source of important claims.
4. Separate confirmed requirements from assumptions and open questions.
5. Do not invent quality targets, integrations, scale, or compliance needs.

If requirements are incomplete, continue with clearly labeled assumptions and
list the missing information that could change the decision.

### 2. Analyze requirements

Organize the findings into:

- Functional requirements and key use cases.
- User roles and authorization boundaries.
- Data entities, ownership, lifecycle, and consistency needs.
- External integrations and provider dependencies.
- Non-functional requirements: performance, scalability, availability,
  reliability, security, privacy, accessibility, maintainability, cost, and
  operability.
- Technical, organizational, regulatory, deployment, and budget constraints.

Identify architectural drivers: requirements that materially distinguish one
architecture from another. Rank them by importance when possible.

### 3. Define viable architecture options

Propose at least **three materially different options**. Include a short
description of each option's:

- Components or modules.
- Communication style.
- Data ownership and persistence strategy.
- Deployment and scaling model.
- Failure and recovery behavior.
- Fit with the requirements.

Do not compare labels alone. Explain how each option would implement the
system's most important workflows.

### 4. Compare trade-offs

Use a comparison table with criteria that matter for this system. At minimum,
consider:

| Criterion | Questions |
|---|---|
| Scalability | What scales, how selectively, and at what cost? |
| Complexity | What must developers and operators build and maintain? |
| Reliability | How are failures isolated, retried, and observed? |
| Consistency | Which operations are transactional or eventually consistent? |
| Performance | Where are latency and throughput limits likely to occur? |
| Security | Where are identity, authorization, secrets, and trust boundaries? |
| Operability | How are deployment, monitoring, backups, and recovery handled? |
| Team fit | Does the design match team size, skills, and ownership? |
| Cost | What infrastructure and maintenance burden does it introduce? |
| Evolution | Can components be changed or extracted later? |

Explain both benefits and costs. Do not treat scalability or flexibility as
free advantages.

### 5. Walk through important scenarios

For each leading option, describe at least one normal flow and one failure
flow. Include scenarios such as:

- A core write followed by a dependent operation.
- An external provider timing out or becoming unavailable.
- A duplicate request or retry.
- A data-store or worker failure.

State what the user sees and whether data can be lost, duplicated, delayed, or
temporarily stale. If multiple services or asynchronous events are involved,
address idempotency, ordering, retries, dead-letter handling, and partial
success explicitly.

### 6. Select the architecture

Choose the option that best satisfies the highest-priority drivers, not the
option with the most features. State:

- The decision in one clear sentence.
- The main reasons it fits the current evidence.
- The important trade-offs accepted.
- The safeguards or mitigations required.
- Conditions that would trigger reconsideration.

Prefer a simple architecture when requirements do not justify distributed
complexity. Allow incremental evolution, such as adding workers, queues,
caching, replicas, or a search index before extracting services.

### 7. Create or update the ADR

Write an ADR with these sections:

1. **Title and metadata:** status, date, scope, and decision owners if known.
2. **Context:** system purpose, constraints, requirements, and uncertainty.
3. **Decision drivers:** the quality attributes and constraints that matter.
4. **Options considered:** at least three options and their implications.
5. **Decision:** the selected architecture and its boundaries.
6. **Architecture overview:** components, communication, data stores, and
   external systems. Use Mermaid when a diagram improves understanding.
7. **Rationale and consequences:** benefits, disadvantages, and accepted
   trade-offs without repeating the same content.
8. **Key workflows:** at least one normal and one failure or retry example.
9. **Implementation challenges and safeguards:** security, data consistency,
   external integrations, operations, testing, and observability.
10. **Reconsideration triggers:** measurable changes that could invalidate the
    decision.

Keep the ADR concise enough to review. Use tables and diagrams when they
communicate more clearly than repeated prose. Avoid implementation details that
are not supported by the requirements.

### 8. Review the ADR

Inspect the completed ADR for:

- A decision that is unambiguous and consistent with the requirements.
- At least three genuinely compared options.
- Explicit scalability, complexity, reliability, consistency, security, and
  cost trade-offs.
- Clear ownership of data and responsibilities.
- Normal and failure workflows.
- No unsupported certainty or hidden assumptions.
- No duplicated or contradictory sections.
- Diagrams that use valid, distinct identifiers and render in the target
  Markdown viewer.
- Reconsideration triggers that are observable rather than vague.

Ask for or apply focused revisions when the ADR is missing evidence, examples,
visual structure, or important consequences. Preserve the decision history
when revising an existing ADR.

## Output style

- Use simple, direct language unless the audience requests deeper detail.
- Label assumptions, unknowns, and recommendations.
- Explain technical terms the first time they appear.
- Prefer concrete examples over generic claims.
- Never claim a requirement, test, or validation that was not actually
  inspected or performed.
- If the user asks for notes, record decisions, alternatives, advantages,
  disadvantages, trade-offs, implementation challenges, and conclusions as the
  work progresses.
