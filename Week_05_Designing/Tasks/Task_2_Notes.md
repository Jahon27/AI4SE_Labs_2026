# Task 2 Discussion Notes

## Note 1: Task 2 started

The user requested an Architecture Decision Record based on the RecipeCove
architecture discussion from Task 1. The compared options are Modular Monolith,
Microservices, and Event-Driven Architecture. The selected direction is a
Modular Monolith with selective event-driven features.

Required first-version files:

- `Task_2_ADR.md`
- `Task_2_Notes.md`

The user asked to continue taking notes throughout Task 2 and plans to review
and improve the ADR later.

## Note 2: Decision context

RecipeCove is a modest web application for recipe discovery, recipe and
ingredient information, Google-based registration/login, favorites, calendars,
recipe events, and diet-based chatbot suggestions. The requirements do not
currently establish high traffic, multiple teams, independent deployments, or
strict availability targets.

The architecture must keep core user operations reliable and understandable
while isolating slow or unreliable external integrations.

## Note 3: Selected architecture

The first ADR version selects a modular monolith with these logical modules:

- Identity and Accounts.
- Recipe Catalog.
- Recipe Search.
- Favorites.
- Calendar.
- Chatbot and Recommendations.
- Optional Notifications/Workers.

The initial persistence strategy is one relational database with module-owned
tables and explicit interfaces. Modules must not directly modify one another's
tables or internal classes.

## Note 4: Selective event-driven features

Event-driven techniques are useful for reminders, notifications,
recommendation updates, analytics, search-index updates, and chatbot jobs.
Core operations that require immediate confirmation remain synchronous.

A bounded worker, scheduler, small queue, or transactional outbox can be added
when the reliability or scale requirements justify it. The entire system does
not need to become a fully event-driven distributed architecture.

## Note 5: Main trade-offs

The chosen approach accepts shared deployment and less selective scaling in
exchange for simpler development, lower operational cost, easier debugging, and
stronger local transactions.

Microservices would provide stronger independent scaling and fault isolation,
but would add network failures, distributed authentication, eventual
consistency, cross-service workflow complexity, and significant deployment and
observability overhead.

A fully event-driven architecture would support loose coupling and asynchronous
work, but would add duplicate and out-of-order event handling, retries,
schema-versioning concerns, broker operations, and harder debugging.

## Note 6: Main implementation challenges

The most important implementation challenges are:

- Enforcing module boundaries and data ownership.
- Implementing Google OAuth/OIDC safely.
- Isolating chatbot resources with timeouts, rate limits, circuit breakers,
  worker limits, and a fallback.
- Keeping recipe search and database queries performant.
- Making favorites, calendar operations, and reminders idempotent.
- Testing external failures and background processing.
- Adding sufficient logging, metrics, and monitoring.

## Note 7: Future review triggers

The decision should be reconsidered if measured traffic requires independent
scaling, chatbot work cannot safely share resources, multiple teams need
independent deployments, the database becomes a measured bottleneck, or stricter
availability and isolation requirements emerge.

The ADR is intentionally a first version for later review and refinement.

## Note 8: ADR diagram and comparison refinement

The user reviewed the first ADR and requested two improvements:

- Replace the text-based architecture diagram with a Mermaid diagram showing
  the RecipeCove modules, relational database, Google login, chatbot provider,
  and background worker.
- Make the architecture comparison table more detailed, especially for
  scalability, complexity, and reliability.

The ADR was updated with the Mermaid diagram and a comparison table that
explicitly describes scaling behavior, implementation complexity, reliability,
consistency, benefits, and costs for all three options.

## Note 9: Mermaid and concision refinement

The Mermaid diagram used `APP` both as a node identifier and as the subgraph
identifier. This was changed to separate identifiers: `RC` for the
RecipeCove application boundary and `MODULES` for the module subgraph. This
avoids an ambiguous Mermaid reference and should render more reliably in VS
Code.

The ADR was made more concise by merging repeated rationale and consequence
sections. A simple user flow was added: recipe search, favorite creation,
calendar-event creation, and background reminder processing. The flow also
documents that favorites and calendar actions are separate commands, so a
calendar failure does not erase a successfully saved favorite.

## Note 10: Final ADR approval and conversation record

The user approved the current ADR as the final version and requested
verification that `Task_2_ADR.md` and `Task_2_Notes.md` remain in the
Task 2 folder. The user also requested `Task_2_Conversation.md` containing the
actual Task 2 requests and assistant responses in chronological order.

The conversation file was generated from the stored session event log. No
messages were reconstructed or invented.
