# Task 1 Notes

All discussion notes recorded during the RecipeCove architecture discussion.

**Total notes: 13**

## Note 1: assignment

**Recorded:** 2026-10-29 19:35:12

User requests ongoing notes covering key points, architectural decisions, advantages, disadvantages, technical trade-offs, implementation challenges, and conclusions. Initial request: inspect the /data folder and list all available software requirements files. Do not design until the assigned project is provided.

## Note 2: inspection

**Recorded:** 2026-10-29 19:35:19

Repository inspection found no literal top-level /data folder. Requirements-related data is under Week_04_Requirements/Task_1/data and Week_05_Designing/Tasks/data. Week_04 contains requirements_output.md plus a source corpus of emails, interviews, meeting notes, survey results, and reference text. Week_05 contains eight project requirement/specification text files. No design work has been started.

## Note 3: project-assignment

**Recorded:** 2026-10-29 19:38:31

Assigned project is RecipeCove. User requests a careful requirements analysis before any architecture proposals, covering purpose, functional and non-functional requirements, features, roles, technical constraints, and unclear or missing requirements, in simple English. Continue taking notes throughout.

## Note 4: requirements-analysis

**Recorded:** 2026-10-29 19:38:40

RecipeCove purpose: a web application for discovering recipes, viewing detailed recipe and ingredient information, bookmarking favorites, and planning recipe-related reminders in a calendar. A chatbot suggests recipes for a specific diet. Roles: visitor and registered user. Explicit visitor functions: Google external registration, recipe-name search, recipe details, ingredient details, diet-based suggested recipes. Explicit registered-user functions: login, logout, profile viewing, create/delete calendar, add calendar events for recipes, add/remove favorites, view favorites. Explicit non-functional requirements: none stated; easy-to-use is a stated goal but has no measurable usability target. Technical constraints/implied integrations: web application, Google external-account registration, chatbot/diet recommendation capability, persistent user profiles/favorites/calendars/events, recipe and ingredient data, authenticated access control, and likely date/time handling for reminders. Open questions affecting architecture: whether anonymous users can browse all content; Google OAuth details and other login methods; chatbot provider/model, diet taxonomy, recommendation behavior, and fallback; recipe/ingredient data source, ownership, schema, updates, search scale, and moderation; profile fields and privacy; calendar multiplicity, sharing, recurrence, time zones, event editing/deletion, notifications, and calendar interoperability; favorite uniqueness and behavior if recipes change; authorization and account deletion; availability/performance/security/accessibility targets; supported browsers/devices/languages; deployment, budget, compliance, observability, backup/recovery, and external API limits. No architecture proposed yet.

## Note 5: conclusion

**Recorded:** 2026-10-29 19:38:40

Current conclusion: requirements are sufficient to identify the product scope and two user roles, but insufficient to choose an architecture confidently without clarifying integrations, data ownership, quality attributes, and calendar/chatbot behavior.

## Note 6: architecture-decision

**Recorded:** 2026-10-29 19:51:29

Candidate architecture discussed: modular monolith for RecipeCove because the current scope appears modest. Proposed modules: Identity/Accounts, Recipe Catalog, Search, Recommendations/Chatbot, Favorites, Calendar, and optionally Notifications/Integration. Modules run in one deployable application and communicate through explicit application services/interfaces and internal commands/events, not direct access to one another's internals. Recommended initial persistence: one relational database with module-owned tables and strict ownership; separate database is not initially necessary. External integrations: Google OAuth/OIDC handled behind an identity adapter; chatbot provider handled behind a recommendation/chatbot adapter. Strengths: simple deployment and local development, low operational cost, easy transactions, fast in-process calls, simpler debugging, suitable for small team and uncertain scale. Weaknesses: shared runtime/database can allow coupling, one deployment affects all modules, scaling is less selective, module boundaries can erode, external chatbot/auth failures still affect user flows if not isolated. Coding challenges: enforcing module boundaries, designing stable interfaces, authentication callback/state/nonce/token handling and account linking, chatbot prompt/data grounding/validation/timeouts/retries/cost/rate limits/fallback, transaction consistency for favorites and calendar, migrations and test coverage. Example flow: authenticated user searches recipe; Search calls Recipe Catalog; user selects favorite and calendar action; Favorites validates identity and recipe reference then inserts unique user-recipe row; Calendar creates event referencing recipe ID; one transaction may save both local records if the UX treats the action as atomic, or separate commands with clear partial-failure feedback. No final architecture commitment yet; this is the first candidate architecture.

## Note 7: trade-offs

**Recorded:** 2026-10-29 19:51:29

Modular monolith trade-off: choose simpler deployment and stronger transactional consistency now, while preserving future extraction options through module-owned data and explicit interfaces. Avoid premature multiple databases or microservices until scale, team boundaries, or independent deployment needs justify them.

## Note 8: scaling-reliability

**Recorded:** 2026-10-29 19:55:11

Important clarification: a chatbot problem does not automatically make the whole modular monolith fail. It can affect other features if chatbot work shares web-process threads/CPU/memory, database connections, request limits, or unbounded waits. Mitigations without adopting microservices: strict chatbot timeouts; bounded concurrency and queue limits; rate limits and per-user quotas; circuit breaker; bulkhead isolation; asynchronous job/worker processing; separate worker process using the same modular code (still one codebase and often one deployable system, but isolated runtime resources); fallback to normal diet-filtered search; caching; cancellation; monitoring and load testing. Protect search/calendar with separate resource pools and priority limits where practical. One relational database can support many users if indexed and designed correctly, but may become a bottleneck through CPU/IO, connection exhaustion, locks, storage, backup/restore time, or single-node availability. Mitigations: proper indexes and pagination, bounded connection pools, query optimization, caching, read replicas for read-heavy catalog/search workloads, partitioning/archiving if needed, database high availability and backups, and possibly a separate search index. Keep module-owned tables and avoid premature database-per-module. Later database separation or service extraction is possible if measured demand justifies it. Key trade-off: isolate expensive chatbot runtime and optimize the shared database before introducing microservices; complexity increases gradually based on evidence.

## Note 9: architecture-candidate-2

**Recorded:** 2026-10-29 19:57:07

Second candidate architecture: microservices for RecipeCove. Possible services: Identity/Accounts, Recipe Catalog, Search, Favorites, Calendar, Recommendations/Chatbot, and Notifications. Each service owns its data and exposes APIs; communication uses HTTP/gRPC for immediate requests and messaging for asynchronous work. A database per service is the preferred ownership model, but shared infrastructure or a transitional shared database is possible and weakens isolation. Advantages over modular monolith: independent deployment and scaling, stronger fault/resource isolation, chatbot can scale separately, technology flexibility, clearer team ownership. Disadvantages: distributed-system complexity, network latency/failures, eventual consistency, more infrastructure/operations, harder local development/debugging/testing, higher cost, duplicated data and cross-service workflows. Chatbot performance improves through independent worker/service scaling, queues, rate limits, circuit breakers, and dedicated resources, but external AI latency remains. Failure behavior: service failure should be isolated where possible; search can remain available if chatbot fails, but favorites/calendar may fail if Identity or Catalog dependencies are unavailable; use timeouts, retries with limits, circuit breakers, fallbacks, cached/read-only data, health checks, observability, and graceful degradation. Hardest implementation areas: service boundaries and data ownership, distributed authentication/authorization, reliable cross-service workflows (favorite + calendar), consistency and event delivery, API/version management, deployment/monitoring/tracing, security, and chatbot provider integration. Current conclusion: microservices offer scaling and isolation but appear disproportionate for the stated RecipeCove scope unless high scale, independent team ownership, or strict availability/isolation requirements are confirmed; modular monolith remains the simpler initial choice. No final architecture selected.

## Note 10: distributed-consistency

**Recorded:** 2026-10-29 20:07:39

Cross-service failure scenario: if Favorites succeeds but Calendar fails, do not pretend both succeeded. Preferred RecipeCove behavior is to treat favorite and calendar scheduling as separate user actions unless requirements explicitly demand atomicity: persist the favorite, report calendar failure clearly, and allow retrying only calendar creation. Prevent duplicates with database unique constraints and idempotency keys/request IDs for both operations. If a single combined action is later required, use a saga/workflow with explicit states, retries, durable commands/events via transactional outbox, and possibly compensation (remove favorite if business policy requires all-or-nothing), recognizing that distributed rollback is not a true atomic transaction and compensation can itself fail. Calendar service should own event uniqueness/idempotency and safely return the existing event on a repeated request. Current recommendation: this consistency complexity is not worth adopting microservices for the currently modest RecipeCove scope; a modular monolith with one relational transaction and resource-isolated chatbot worker is simpler and safer. Microservices would be justified only by demonstrated scale, independent deployment/team ownership, or strict isolation requirements.

## Note 11: architecture-candidate-3

**Recorded:** 2026-10-29 20:09:39

Third candidate architecture: event-driven architecture for RecipeCove. Modules/services publish domain events such as FavoriteAdded, FavoriteRemoved, CalendarCreated, RecipeEventScheduled, RecipeUpdated, and UserRegistered to a broker; consumers such as Notifications, Recommendations, Search indexing, analytics, or audit processing react asynchronously. The initiating command should persist its local state and reliably publish an event, ideally with a transactional outbox. Event-driven style can be combined with a modular monolith or microservices; it is not automatically a separate deployment architecture. Advantages: loose coupling, easy addition of consumers, asynchronous work, useful for notifications/search indexing/recommendation updates, buffering and retrying chatbot or reminder work. Disadvantages: eventual consistency, harder debugging/testing, duplicate/out-of-order messages, broker operational cost, schema/version management, unclear user feedback for async operations, and overengineering for simple synchronous features. Favorites and calendar actions should remain synchronous when immediate confirmation is required; publish events after successful local transactions for optional downstream work. Hardest implementation areas: reliable delivery, idempotent consumers, ordering, retries/dead-letter queues, event schema evolution, observability/correlation IDs, and deciding which actions truly need asynchronous processing. Current recommendation: use event-driven patterns selectively inside a modular monolith (in-process events or a small queue/outbox for notifications, chatbot jobs, and calendar reminders), not a full event-driven distributed system for all RecipeCove behavior. No final architecture selected.

## Note 12: reminder-reliability

**Recorded:** 2026-10-29 20:11:03

Reminder reliability decision: true exactly-once delivery across a broker and external notification provider cannot generally be guaranteed; target effectively-once user-visible reminders. Store a durable reminder record with a stable reminder/event ID and status, publish through a transactional outbox, use at-least-once delivery with retries, and make the reminder consumer idempotent using a unique constraint/deduplication record on reminder_id plus provider idempotency support where available. Claim work safely, mark sent only after provider confirmation, and use reconciliation for ambiguous timeouts. Avoid sending duplicate reminders after crashes; acknowledge only after durable processing. If the provider lacks idempotency, exact duplicate prevention cannot be guaranteed, so use a simple in-app reminder or clearly document the limitation. For this small project, a full broker/event-driven system is likely overcomplicated. Recommended simpler design: Calendar module stores reminder/event and an in-process or bounded background scheduler queries due reminders, atomically claims each reminder, sends once, records status, retries failures, and provides monitoring; add a queue/outbox only if scale or reliability requirements justify it.

## Note 13: final-decision

**Recorded:** 2026-10-29 20:12:59

Final recommendation for RecipeCove: choose a modular monolith as the primary architecture, using one relational database with strict module-owned tables and explicit interfaces. Add selective event-driven techniques only where useful: a bounded background worker/scheduler for chatbot and reminders, optional internal events, and an outbox/queue only when scale or reliability justifies it. Reasons: current scope is modest, requirements do not establish high scale, multiple teams, independent deployments, or strict isolation; modular monolith minimizes operational and distributed-consistency complexity while preserving future extraction paths. Microservices are less suitable now because they add network failures, distributed authentication, data ownership, eventual consistency, cross-service workflows, deployment/observability overhead, and difficult partial-failure handling. A fully event-driven architecture is less suitable as the default because core user operations need immediate confirmation and events introduce eventual consistency, duplicate/out-of-order delivery, schema evolution, broker operations, and harder debugging. Main implementation challenges for chosen approach: enforce module boundaries, implement Google OAuth/OIDC safely, isolate chatbot resources with timeouts/rate limits/circuit breaker/worker/fallback, design recipe search and database indexes, implement idempotent favorites/calendar/reminder operations, and monitor failures. Final trade-off: accept shared deployment/database and less independent scaling in exchange for simplicity, transactions, lower cost, and easier development; evolve incrementally based on measured demand.
