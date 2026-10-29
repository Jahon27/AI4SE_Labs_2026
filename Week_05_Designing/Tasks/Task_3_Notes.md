# Task 3 Discussion Notes

## Note 1: Repeat-session scope

The architecture-decision Skill was applied to the RecipeCove requirements.
The repeat exercise must:

- Read the actual `RecipeCove.txt` requirements.
- Compare three architecture options.
- Explain advantages, disadvantages, trade-offs, and implementation
  challenges.
- Recommend the best option.
- Create an ADR.
- Preserve Task 1 and Task 2 files.

## Note 2: Requirements evidence

RecipeCove is a web application for recipe discovery and ingredient
information. Visitors search by recipe name, view recipes and ingredients, and
receive diet-based chatbot suggestions. Registered users log in, view profiles,
manage favorites, create/delete calendars, and add recipe events.

Explicit quality targets are missing. Important unresolved questions include
recipe data ownership, chatbot behavior and provider, calendar/reminder
semantics, expected scale, performance, availability, privacy, accessibility,
and notification requirements.

## Note 3: Architecture options

The three options compared are:

1. **Modular monolith:** one application with explicit modules and one
   relational database; bounded workers handle chatbot and reminders.
2. **Microservices:** independently deployed identity, recipe, search,
   favorites, calendar, and chatbot services with service-owned data.
3. **Fully event-driven architecture:** a broker and asynchronous consumers
   process events for core and background operations.

## Note 4: Decision and trade-offs

The recommendation is a modular monolith with selective event-driven features.
It best fits the current evidence because it provides simple deployment,
transactional core operations, low cost, and a future extraction path.

The accepted disadvantages are shared deployment/database resources and less
selective scaling. Microservices are deferred because the requirements do not
justify distributed-system complexity. A fully event-driven default is
deferred because immediate user confirmation is more important for core
favorites and calendar operations.

## Note 5: Implementation challenges

The main challenges are Google OAuth/OIDC correctness, chatbot timeout and
failure isolation, module-boundary enforcement, database/search performance,
idempotent favorite/calendar/reminder operations, and testing/observability.

The ADR records safeguards including bounded workers, timeouts, rate limits,
circuit breakers, fallback search, indexes, pagination, stable request IDs,
durable reminder records, retries, and monitoring.

## Note 6: Deliverables

Created without overwriting earlier work:

- `Task_3_ADR.md`
- `Task_3_Notes.md`
- `Task_3_Conversation.md`
- `Task_3_Comparison.md`

The ADR includes metadata, context, drivers, three options, a detailed
comparison table, Mermaid overview, decision, consequences, workflow and
failure behavior, implementation safeguards, open requirements, and
reconsideration triggers.
