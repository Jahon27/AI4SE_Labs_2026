# Software Requirements Specification

## Priority scale

- **must**: Required for the system to be acceptable; failure blocks a core business or legal need.
- **should**: Important and expected, but a temporary workaround is possible.
- **could**: Useful enhancement that can be postponed without blocking delivery.
- **deferred**: Identified need intentionally postponed pending clarification or later scope.

## Requirements

### REQ-001: Material volume report scoped to a library/location
**Priority:** `must`  
**Category:** Reporting  
**Derived from:** conv_pines014_material_volume.eml, early_draft_srs_galecia.txt

The system must provide a material volume report that returns item counts scoped to a specified library/location using the library/location assignment on items.

**Rationale:** The thread explicitly required per-library counts (e.g., counts where location equals the selected library).

### REQ-002: Material volume report provides acquisitions, on-shelf, in-circulation, and total
**Priority:** `must`  
**Category:** Reporting  
**Derived from:** conv_pines014_material_volume.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must provide, in a single material volume report, separate numeric counts for (a) new acquisitions, (b) items on the shelf (checked-in), (c) items in circulation (checked out), and (d) total owned items for the scoped library.

**Rationale:** Participants requested both component counts and a total in one consolidated view for management use.

### REQ-003: Material volume totals include checked-out items
**Priority:** `must`  
**Category:** Business rule  
**Derived from:** conv_pines014_material_volume.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The total item count in the material volume report for a scoped library must include items whose status indicates they are currently checked out (i.e., the total reflects all owned statuses included in the report components).

**Rationale:** The discussion included an open question, and the supported outcome implied that checked-out items should be included in totals for collection management.

### REQ-004: Material volume report includes current hold counts
**Priority:** `must`  
**Category:** Reporting  
**Derived from:** conv_pines014_material_volume.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The material volume report must include an explicit numeric field for the number of current holds for the scoped library.

**Rationale:** Holds were repeatedly requested as a required component of material volume reporting.

### REQ-005: Material volume report breakdown supports genre and format and other category breakdowns
**Priority:** `must`  
**Category:** Reporting / Data model  
**Derived from:** conv_pines014_material_volume.eml, conv_pines016_shelf_space.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The material volume report must present metrics broken down by both genre and material format (genre × format combinations) and must support additional category breakdowns configured for the report.

**Rationale:** The core request required breakdown by genre and format, and other categories were expected to be configurable.

### REQ-006: Material volume report has configurable category breakdowns
**Priority:** `should`  
**Category:** UI/Customization  
**Derived from:** conv_pines014_material_volume.eml

The system must allow users/administrators to configure the category breakdowns used in the material volume report by adding, removing, or renaming categories and by selecting which catalog metadata field(s) determine category membership.

**Rationale:** Participants raised the need for library-specific category breakdowns.

### REQ-007: Material volume report supports grouping by multiple classification dimensions
**Priority:** `should`  
**Category:** Reporting  
**Derived from:** conv_pines014_material_volume.eml, early_draft_srs_galecia.txt

The material volume report must support grouping and reporting by multiple classification dimensions (e.g., fiction/non-fiction, format, genre, and other configured cataloging fields).

**Rationale:** A multi-dimensional grouping capability was proposed for more meaningful collection management breakdowns.

### REQ-008: Material volume report supports point-in-time volume queries
**Priority:** `should`  
**Category:** Filtering/Time-series  
**Derived from:** conv_pines014_material_volume.eml, early_draft_srs_galecia.txt

The system must allow users to generate the material volume report as of a specified point in time using a user-provided date (or date/time).

**Rationale:** Participants requested date filters and historical comparisons for volume at any point in time.

### REQ-009: Material volume acquisition/time filters use the acquisition date field
**Priority:** `must`  
**Category:** Data model  
**Derived from:** conv_pines014_material_volume.eml, early_draft_srs_galecia.txt

The system must use the item acquisition date field to determine new acquisitions for acquisition-based time filters and period-based reporting in material volume reports.

**Rationale:** The thread confirmed acquisition date tracking and that time-based acquisition reporting depends on it.

### REQ-010: Material volume report supports period-based acquisition/delta reporting
**Priority:** `should`  
**Category:** Filtering/Time-series  
**Derived from:** conv_pines014_material_volume.eml, early_draft_srs_galecia.txt

The system must support period-based material volume queries that return counts of items added (new acquisitions) within a specified time window and optionally the change in volume over that period.

**Rationale:** Users requested last 30/60/90 day additions for collection management.

### REQ-011: Material volume report is a single consolidated output view
**Priority:** `must`  
**Category:** Usability/Reporting  
**Derived from:** conv_pines014_material_volume.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must provide a single consolidated material volume report output view containing all requested counts and breakdowns so users do not need to manually combine data from multiple screens.

**Rationale:** Participants explicitly requested one consolidated report rather than manual assembly from multiple screens.

### REQ-012: Capacity overview dashboard for all branches
**Priority:** `must`  
**Category:** UI/Reporting  
**Derived from:** conv_pines015_capacity_interface.eml, early_draft_srs_galecia.txt

The system must provide a capacity overview dashboard that displays capacity metrics for all branches in a single view.

**Rationale:** Branch manager requested a system-wide view of capacity, not just a single branch.

### REQ-013: Capacity drill-down to individual branch details
**Priority:** `must`  
**Category:** UI/Reporting  
**Derived from:** conv_pines015_capacity_interface.eml, early_draft_srs_galecia.txt

The system must provide the ability to drill down from the capacity overview dashboard to an individual branch detail view that shows that branch’s capacity metrics.

**Rationale:** Users need branch-specific metrics after seeing system-wide status.

### REQ-014: Capacity dashboard supports filtering and grouping for scale
**Priority:** `must`  
**Category:** Usability/Performance  
**Derived from:** conv_pines015_capacity_interface.eml, early_draft_srs_galecia.txt

The capacity interface must support filtering branches by region, library type, and current load, and must support grouping/aggregation (e.g., by system or region) so the overview remains usable when there are many locations.

**Rationale:** Participants explicitly requested filters and scale handling for a large number of branches.

### REQ-015: Capacity interface supports sorting by metrics
**Priority:** `should`  
**Category:** UI/Interaction  
**Derived from:** conv_pines015_capacity_interface.eml

The capacity interface should allow users to sort the displayed branches by any visible numerical capacity metric shown in the current view.

**Rationale:** Sorting was requested to help users identify priority branches quickly.

### REQ-016: Capacity interface exports current view to CSV
**Priority:** `must`  
**Category:** Reporting/Export  
**Derived from:** conv_pines015_capacity_interface.eml, early_draft_srs_galecia.txt

The system must provide an export function that writes the currently displayed branch data (respecting the current filters and sorts) to a CSV file.

**Rationale:** Directors wanted spreadsheets; export to CSV was explicitly requested.

### REQ-017: Capacity interface includes capacity trend data
**Priority:** `should`  
**Category:** Reporting/Analytics  
**Derived from:** conv_pines015_capacity_interface.eml

The capacity interface should display trend data indicating whether each branch is growing or shrinking over time, accessible from the overview or branch detail.

**Rationale:** Long-term planning requires visibility into growth/shrink patterns.

### REQ-018: Capacity interface shows color-coded status with configurable thresholds
**Priority:** `should`  
**Category:** UI/Visualization  
**Derived from:** conv_pines015_capacity_interface.eml

The capacity interface should present a color-coded status indicator for branch capacity (e.g., under capacity, approaching capacity, at/over capacity) using administrator-configurable numeric thresholds.

**Rationale:** Color-coding was proposed, and thresholds must be configurable for consistent meaning across branches/metrics.

### REQ-019: Capacity metric definitions are configurable by administrators
**Priority:** `must`  
**Category:** Configuration/Data  
**Derived from:** conv_pines015_capacity_interface.eml

Administrators must be able to select/configure what capacity metric(s) define “capacity” for reporting and visualization, supporting at minimum options such as item count vs shelf space, physical item count vs a configured limit, and circulation volume vs processing capacity.

**Rationale:** Participants noted capacity needed definition before building the interface.

### REQ-020: Capacity interface aggregates centralized data for all branches
**Priority:** `must`  
**Category:** Data/Integration  
**Derived from:** conv_pines015_capacity_interface.eml

The system must obtain and aggregate capacity data for all branches from the centralized database so that the overview and drill-downs reflect current centralized data.

**Rationale:** Technical discussion confirmed central database aggregation.

### REQ-021: Shelf-space report computes circulation, collection, and shelf-space percentages by genre and format
**Priority:** `must`  
**Category:** Reporting / Data calculation  
**Derived from:** conv_pines016_shelf_space.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

For a specified scope (single library or entire system) and a selected snapshot date or defined collection period, the system must calculate for each genre × material format combination: (a) percentage of circulations represented by that group within the selected date range, (b) percentage of collection represented by that group within the snapshot/period, and (c) percentage of total shelf space occupied by that group using an estimation approach selected for the report.

**Rationale:** Participants requested a combined shelf-space analysis comparing usage, holdings, and shelf-space allocation by genre and format.

### REQ-022: Shelf-space percentages computed from existing database fields and calculations
**Priority:** `must`  
**Category:** Data calculation / Integration  
**Derived from:** conv_pines016_shelf_space.eml

The shelf-space report must compute item counts per genre × format and sum checkouts per genre × format from existing catalog and circulation data sources (or other configured data sources) for the selected scope and date range; these computed values must be the basis for the reported percentages.

**Rationale:** The report needs database-backed counts/sums as the foundation for percentage calculations.

### REQ-023: Shelf-space report supports per-library and per-system scopes
**Priority:** `must`  
**Category:** Reporting / Aggregation  
**Derived from:** conv_pines016_shelf_space.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

The system must allow generating the shelf-space report for either a single library (branch) or for the entire system (aggregated across all libraries), computing the same metrics for the selected scope.

**Rationale:** Branch managers and directors required both local and system views.

### REQ-024: Shelf-space report date-range filtering for circulation metrics
**Priority:** `should`  
**Category:** Filtering / Reporting  
**Derived from:** conv_pines016_shelf_space.eml

The system should allow users to restrict the circulations included in the shelf-space report to an arbitrary date range (custom start/end or standard periods) when computing circulation percentage metrics.

**Rationale:** Circumstances vary by season; users need date range comparisons.

### REQ-025: Shelf-space report supports shelf-space estimation method selection and documentation
**Priority:** `should`  
**Category:** Reporting / UI  
**Derived from:** conv_pines016_shelf_space.eml

The shelf-space report must provide a user-selectable shelf-space estimation method when dimensions are unavailable, and must document in the report output which method was used (e.g., dimensions-based when available, or item-count proxy when not).

**Rationale:** The report requires either dimensions-based precision or a proxy estimate, and users need transparency.

### REQ-026: Missing and damaged items report per branch and system
**Priority:** `must`  
**Category:** Reporting  
**Derived from:** conv_pines019_020_missing_intransit.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must generate a missing-and-damaged items report listing items recorded as missing or damaged, grouped by branch, and support running the report for an individual branch or for the entire system.

**Rationale:** Front-line and management users required per-branch investigation and system-wide visibility.

### REQ-027: Missing and damaged items report includes condition notes
**Priority:** `should`  
**Category:** Data  
**Derived from:** conv_pines019_020_missing_intransit.eml

The missing-and-damaged items report must include recorded condition notes for each item (free-text and/or coded notes such as water damage or vandalism).

**Rationale:** Users requested condition notes to help identify causes and patterns.

### REQ-028: Missing and damaged items report supports date-range filtering and status filtering
**Priority:** `should`  
**Category:** Reporting  
**Derived from:** conv_pines019_020_missing_intransit.eml

The missing-and-damaged items report must support date-range filtering of results and filtering by recorded item status values (e.g., missing, lost, damaged, and long-overdue).

**Rationale:** Date-range and status filtering were requested for audit/trending use cases.

### REQ-029: Missing and damaged items report includes counts by title
**Priority:** `should`  
**Category:** Reporting  
**Derived from:** conv_pines019_020_missing_intransit.eml

The missing-and-damaged items report should provide counts of missing/damaged occurrences grouped by title.

**Rationale:** Users wanted repeat-loss/damage signals by title for collection decisions.

### REQ-030: In-transit items aged report (merge to/from) per branch and system
**Priority:** `must`  
**Category:** Reporting/Configuration  
**Derived from:** conv_pines019_020_missing_intransit.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must generate an in-transit items report that merges transit-to and transit-from records into a single view, lists items in transit longer than a configurable threshold X (default 7), and supports running it for an individual branch or for the entire system.

**Rationale:** Front-line staff requested a single merged in-transit report with a configurable aging threshold.

### REQ-031: In-transit report defines inclusion using arrival/departure and X-days threshold
**Priority:** `should`  
**Category:** Technical  
**Derived from:** conv_pines019_020_missing_intransit.eml

For the in-transit report, an item must be considered in-transit if its transit record has no arrival date and its departure date is older than the configured X-day threshold.

**Rationale:** A precise technical definition was required to implement the report correctly.

### REQ-032: In-transit items report supports due-date sorting and optional branch/system filters
**Priority:** `should`  
**Category:** Usability  
**Derived from:** conv_pines019_020_missing_intransit.eml

The in-transit items report should allow sorting results by due date (ascending) and should support filtering by branch and system scope consistent with the report’s scoping controls.

**Rationale:** Staff needed sorting so they address oldest items first.

### REQ-033: Batch candidate query and manual selection workflow for item transfers
**Priority:** `must`  
**Category:** UI / Workflow  
**Derived from:** conv_pines018_item_transfer.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must provide a query-builder interface to locate candidate items for transfer using item-level fields, allow saving and reusing queries, and present query results in a selectable list that supports manual selection/deselection of items before initiating a transfer.

**Rationale:** Users requested query-driven identification plus manual selection before moving items.

### REQ-034: Saved transfer queries are reusable and can be shared
**Priority:** `must`  
**Category:** Reporting  
**Derived from:** conv_pines018_item_transfer.eml, interview_cataloging_2009-05-08.txt

The system must allow users to save constructed item candidate queries as named templates for later reuse, and should allow authorized sharing of saved query templates with other users/groups.

**Rationale:** Repeated monthly use and coordinated workflows implied save and optional share.

### REQ-035: Transfer preview with confirmation and item count/sample export option
**Priority:** `must`  
**Category:** UI / Safety  
**Derived from:** conv_pines018_item_transfer.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

Before applying a transfer, the system must display a preview summarizing the transfer (including total number of items) and require explicit user confirmation to proceed; the preview must allow viewing or exporting the full item list or a representative sample.

**Rationale:** Safety mechanisms were required to prevent accidental mass moves.

### REQ-036: Role-based permission control for transfers
**Priority:** `must`  
**Category:** Security / Admin  
**Derived from:** conv_pines018_item_transfer.eml

The system must enforce role-based permissions so that only authorized users (configurable roles/groups such as managers, administrators, and transfer coordinators) can create, approve, or execute transfers.

**Rationale:** Not all staff should be able to move items; permission enforcement is necessary.

### REQ-037: Atomic, auditable batch update of item location for transfers
**Priority:** `must`  
**Category:** Data / Workflow  
**Derived from:** conv_pines018_item_transfer.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must support performing an atomic and auditable batch update that changes the location field of selected items to a specified destination location.

**Rationale:** Location changes must be transaction-safe and recorded for auditability.

### REQ-038: Transfer metadata includes original location and audit-relevant fields
**Priority:** `must`  
**Category:** Data / Audit  
**Derived from:** conv_pines018_item_transfer.eml, interview_cataloging_2009-05-08.txt

When performing a transfer, the system must record and persist each item’s original location and transfer metadata including initiating user, timestamp, destination, reason, and any scheduled revert settings.

**Rationale:** Accurate reversion and audit depend on recorded original state and transfer context.

### REQ-039: Transfer logging and per-item transfer history
**Priority:** `must`  
**Category:** Audit / Logging  
**Derived from:** conv_pines018_item_transfer.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must log every transfer action and maintain an audit trail recording initiating user, timestamp, items affected, original and new locations, and automated actions; additionally, it must retain per-item transfer history that is queryable and reportable by date and initiating user.

**Rationale:** Participants requested audit trails and the ability to see how often an item was transferred.

### REQ-040: Printable pull lists for transfers
**Priority:** `must`  
**Category:** Logistics / Reporting  
**Derived from:** conv_pines018_item_transfer.eml, early_draft_srs_galecia.txt, interview_cataloging_2009-05-08.txt

The system must generate a printable pull list for a transfer containing item identifiers, titles, barcodes, source locations, and destination, formatted for staff use during physical movement.

**Rationale:** Staff workflow requires a pull list to find items.

### REQ-041: Auto-revert of temporary transfers via configurable scheduled revert
**Priority:** `must`  
**Category:** Automation / Workflow  
**Derived from:** conv_pines018_item_transfer.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must support scheduling an automatic revert of transferred items back to their recorded original location after a configurable time period (X days), with the scheduled revert stored in the transfer metadata.

**Rationale:** Temporary transfers for events/outreach require automated return behavior.

### REQ-042: Scheduled process evaluates transfers with scheduled reverts and performs revert in batches
**Priority:** `must`  
**Category:** Automation / Performance  
**Derived from:** conv_pines018_item_transfer.eml

The system must implement an automated scheduled process that evaluates transfers with scheduled reverts and performs the revert operation, including logging and batch processing to avoid long locks.

**Rationale:** Implementation must be scalable and efficient for large item counts.

### REQ-043: Transfer delay and error alerts to configured recipients
**Priority:** `should`  
**Category:** Monitoring / Notifications  
**Derived from:** conv_pines018_item_transfer.eml

The system should notify configured recipients via email or in-system notifications when a transfer encounters errors, is delayed, or when scheduled automated actions (e.g., auto-revert) fail.

**Rationale:** Operational awareness is needed for transfer success.

### REQ-044: Weeding/purging candidate reporting and safe preview
**Priority:** `must`  
**Category:** Safety  
**Derived from:** conv_pines021_item_purging.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must provide a read-only report that lists candidate items eligible for purging based on user-specified criteria, with no deletions or status changes performed by generating the candidate report.

**Rationale:** A safe candidate list is required before any purge action is executed.

### REQ-045: Purging criteria filters by status, time-in-status, and last-circulated inactivity
**Priority:** `must`  
**Category:** reporting  
**Derived from:** conv_pines021_item_purging.eml

The system must allow users to filter purge candidate item records by (a) item status values, (b) time an item has been in a given status with user-configurable thresholds and units, and (c) last-circulation inactivity thresholds (e.g., not circulated in X days/months/years).

**Rationale:** Multiple criteria-based filters were explicitly requested for purge candidate identification.

### REQ-046: Purging criteria supports Boolean combination (AND/OR)
**Priority:** `must`  
**Category:** reporting  
**Derived from:** conv_pines021_item_purging.eml

The system must allow users to combine multiple purge criteria using Boolean logic (AND/OR) to construct compound purge filters.

**Rationale:** Compound filters were requested to express realistic purge rules.

### REQ-047: Batch status conversion for purge candidates with separate confirmation and audit trail
**Priority:** `must`  
**Category:** bulk-edit  
**Derived from:** conv_pines021_item_purging.eml

The system must support executing batch status conversions for sets of items identified by purge candidate reports, but must require a separate explicit confirmation step before applying changes and must write the changes to an audit trail.

**Rationale:** Safety and accountability were emphasized for bulk status changes.

### REQ-048: Last-copy report per branch and system and flagging sole copies
**Priority:** `must`  
**Category:** reporting  
**Derived from:** conv_pines021_item_purging.eml, interview_cataloging_2009-05-08.txt, early_draft_srs_galecia.txt

The system must provide a last-copy report that identifies items that are the only copy within the selected scope, supporting at minimum per-library (branch) and system-wide scopes, and must clearly flag sole-copy items in report outputs.

**Rationale:** Users required a critical safeguard to prevent accidental deletion of unique holdings at both branch and system levels.

### REQ-049: Deletion and cleanup utilities with confirmation and audit trail
**Priority:** `must`  
**Category:** data-cleanup  
**Derived from:** conv_pines021_item_purging.eml

The system must provide utilities to (a) delete volume records together with associated copy/item records upon user confirmation, and (b) identify orphaned bibliographic/volume records with no attached items and delete them upon user confirmation; the system must maintain an audit trail for purge/deletion/batch status conversion actions.

**Rationale:** Users requested batch cleanup tools with safety confirmation and required auditability.

### REQ-050: Separate confirmation step for deletions
**Priority:** `must`  
**Category:** safety  
**Derived from:** conv_pines021_item_purging.eml

The system must require an explicit separate confirmation step before performing any deletion of items, volumes, or bibliographic records, distinct from candidate/report generation.

**Rationale:** Participants insisted on preventing accidental deletions.

### REQ-051: Deletion audit records persist with required fields
**Priority:** `must`  
**Category:** Audit/Logging  
**Derived from:** conv_pines022_deletions.eml, interview_cataloging_2009-05-08.txt

The system must create persistent deletion audit log records for every successful deletion of any record type, and each audit record must include at minimum record_type, record_id, deleted_by (user identifier), deleted_at (timestamp), and location (branch or system).

**Rationale:** The thread required audit logs because deleted records otherwise disappear, and specified required fields for the audit table.

### REQ-052: Deletion audit report interface with aggregations and predefined admin reports
**Priority:** `must`  
**Category:** Reporting  
**Derived from:** conv_pines022_deletions.eml

The system must provide a report/query interface over deletion audit records to produce counts and lists aggregated by date range, user, record type, and location and across the system; it must also provide predefined administrative reports including total deletions per period, deletions by type, deletions by location, and a ranked list of users by number of deletions.

**Rationale:** Administrators needed audit reporting and specific accountability reports.

### REQ-053: Admin report list of deleted patron records filterable by quarter/date range
**Priority:** `must`  
**Category:** Reporting  
**Derived from:** conv_pines022_deletions.eml

The system must allow administrators to produce a list of deleted patron records filtered by record type and date range (e.g., deleted patrons in Q1).

**Rationale:** A specific audit use case was described requiring patron-deletion listing by quarter.

### REQ-054: Patron characteristics reporting supports configurable filters and grouping with AND/OR
**Priority:** `must`  
**Category:** Aggregation  
**Derived from:** conv_pines023_patron_characteristics.eml, early_draft_srs_galecia.txt, survey_results_2009.txt

The system must support reports that can be limited by patron age range, ZIP code, county of residence, home branch, patron type, and preferred language and can group results by the same characteristics; the report query builder must support combining multiple filters using AND and OR logic, include null-demographic records in results, and support LIMIT/WHERE plus GROUP BY/aggregate operations.

**Rationale:** Participants requested a consolidated set of demographic filters and grouping operations with Boolean combination and correct data-quality behavior for null values.

### REQ-055: Patron age ranges computed at query time from birth date
**Priority:** `must`  
**Category:** DataCalculation  
**Derived from:** conv_pines023_patron_characteristics.eml

The system must compute patron age ranges at query time from the birth_date field to enable accurate age-range filtering and grouping.

**Rationale:** Age grouping depends on computing age from birth_date during queries.

### REQ-056: Inactive patrons report with configurable inactivity window and background/cached execution
**Priority:** `must`  
**Category:** functional  
**Derived from:** conv_pines024_inactive_patrons.eml, early_draft_srs_galecia.txt

The system must generate an inactive patrons report listing patrons whose last circulation or electronic activity date is older than X days, where X is configurable; the report must support large datasets via background execution and cached results.

**Rationale:** Core functional requirement plus non-functional constraints were repeatedly requested due to dataset size.

### REQ-057: Inactive patrons electronic activity definition and consolidation across sources
**Priority:** `must`  
**Category:** functional  
**Derived from:** conv_pines024_inactive_patrons.eml

For inactive-patrons evaluation, the system must consider electronic activity as including OPAC/patron logins, online hold placements, and online renewals, and include digital resource access as electronic activity when digital access events are logged/integrated; it must consolidate these events across multiple data sources to compute each patron’s most recent electronic activity date.

**Rationale:** The thread provided explicit definitions and required consolidation across separate tables/logs.

### REQ-058: Inactive patrons report supports configurable grouping levels and includes mailing addresses
**Priority:** `must`  
**Category:** functional  
**Derived from:** conv_pines024_inactive_patrons.eml

The inactive patrons report must allow configurable grouping/level selection including at minimum System, Home Library, and County, and must include the mailing address fields needed for postal outreach (street, city, state, postal code).

**Rationale:** Users required grouping at organizational levels and postal outreach fields for outreach workflows.

### REQ-059: Inactive patrons report is exportable to CSV
**Priority:** `must`  
**Category:** functional  
**Derived from:** conv_pines024_inactive_patrons.eml

The system must export inactive-patrons report results at least in CSV format suitable for upload to external outreach systems.

**Rationale:** Users asked for CSV exports to their outreach platforms.

### REQ-060: System-scale capacity for consortium size and workload
**Priority:** `must`  
**Category:** Non-Functional - Scalability/Performance  
**Derived from:** early_draft_srs_galecia.txt, meeting_2009-07-20_minutes.txt

The system must support a library consortium of at least 286 locations, at least 17,000,000 annual circulations, and at least 900,000 purchased/processed items per year without data loss or functional failure.

**Rationale:** A dedicated scalability requirement was stated as a core testable acceptance condition.

### REQ-061: System supports Linux/Solaris deployment and relational database backend
**Priority:** `must`  
**Category:** Non-Functional  
**Derived from:** early_draft_srs_galecia.txt, interview_sysadmin_2009-05-10.txt, meeting_2009-07-20_minutes.txt, meeting_tech_subcommittee_2009-06-30.txt

The system must be deployable on Linux or Solaris servers and must use a fully relational database backend for persistent storage.

**Rationale:** Operational constraints and architectural assumptions specify environment and relational persistence requirements.

### REQ-062: Management reporting must not constrain OPAC functionality and must use read-only access
**Priority:** `must`  
**Category:** Non-Functional - Integration/Compatibility  
**Derived from:** meeting_tech_subcommittee_2009-06-30.txt, meeting_2009-03-15_minutes.txt, meeting_2009-07-20_minutes.txt, early_draft_srs_galecia.txt

The management reporting subsystem must not constrain/degrade OPAC functionality or responsiveness, and it must access OPAC/ILS data in read-only mode (must not modify OPAC/ILS records as part of reporting).

**Rationale:** Thread notes state patrons require fast catalog access and reports must not impact OPAC operations.

### REQ-063: Reporting searches and report generation run during open hours via background queuing
**Priority:** `must`  
**Category:** Non-Functional - Performance/Availability  
**Derived from:** interview_sysadmin_2009-05-10.txt, meeting_tech_subcommittee_2009-06-30.txt, meeting_2009-07-20_minutes.txt, early_draft_srs_galecia.txt

The system must allow searches and report generation during library open hours without materially disrupting other operational services, using background queuing/processing for complex reports.

**Rationale:** Performance and availability concerns were repeatedly emphasized, with a background queuing mitigation.

### REQ-064: Web UI and HTML output are standards-compliant and accessible to assistive technologies
**Priority:** `must`  
**Category:** Non-Functional - Accessibility  
**Derived from:** early_draft_srs_galecia.txt, interview_sysadmin_2009-05-10.txt, meeting_tech_subcommittee_2009-06-30.txt, meeting_2009-07-20_minutes.txt

All staff-facing web pages and report outputs must produce standards-compliant HTML and must be accessible using assistive technologies (e.g., screen readers and magnification), complying with applicable accessibility requirements such as Section 508.

**Rationale:** Accessibility and HTML standards were explicitly stated as non-negotiable requirements.

## Discarded candidates

- **Candidate:** {'name': 'Hold counts broken down by category', 'statement': 'The report should include hold counts broken down by whatever category breakdown is applied (e.g., holds per category such as adult fiction or board books).', 'priority': 'should', 'category': 'Reporting'}
  **Sources:** conv_pines014_material_volume.eml
  **Reason:** Discarded because it is not atomic relative to the retained requirement that the report supports genre×format and other configurable category breakdowns (REQ-005). Category breakdown capability subsumes holds breakdown behavior without requiring an additional separate requirement.
- **Candidate:** {'name': 'Default category set in report', 'statement': 'The system should provide a default set of categories in the material volume report that includes at minimum: total items, number of holds, adult fiction, and board books.', 'priority': 'should', 'category': 'Reporting'}
  **Sources:** conv_pines014_material_volume.eml
  **Reason:** Discarded as an implementation detail (default category contents) that does not add a distinct capability beyond configurable category breakdowns (REQ-006).
- **Candidate:** {'name': 'Separate counts for acquisitions/checked-in/checked-out and total', 'statement': 'The system must produce, in a single report, separate numeric counts for (a) new acquisitions, (b) items on the shelf (checked in), (c) items out in circulation (checked out), and (d) the total number of items owned by the library.', 'priority': 'must', 'category': 'Reporting'}
  **Sources:** conv_pines014_material_volume.eml
  **Reason:** Merged into REQ-002 as the same capability (component counts plus total in one material volume report).
- **Candidate:** {'name': 'Ambiguity: confirm whether totals should include checked-out items', 'statement': "There is an open/doubtful question to confirm whether the 'total items in library' should count items that are checked out or whether 'total' should mean only items physically present; this must be explicitly specified before implementation if not already decided.", 'priority': 'deferred', 'category': 'Business rule'}
  **Sources:** conv_pines014_material_volume.eml
  **Reason:** Discarded as a clarification artifact; the business rule decision is captured by REQ-003.
- **Candidate:** {'name': 'Export trend/time-series data', 'statement': 'The system should allow exporting the trend/time-series data used to compute growth/shrink patterns (for selected branches or the current view) to CSV.', 'priority': 'should', 'category': 'Reporting/Export'}
  **Sources:** conv_pines015_capacity_interface.eml
  **Reason:** Discarded because the retained requirements already cover CSV export of the current view (REQ-016) and trend display (REQ-017); exporting underlying trend datasets is an enhancement that is not required for core dashboard capability.
- **Candidate:** {'name': 'Show system average and per-library deviation', 'statement': "When generating a per-library report the system should include system-average metrics for the same genre/format categories and calculate or highlight each library's deviation from the system average.", 'priority': 'should', 'category': 'Reporting / Comparison'}
  **Sources:** conv_pines016_shelf_space.eml
  **Reason:** Discarded as non-core relative to the retained atomic calculation/reporting capability (REQ-021) which already defines required metrics; “deviation vs average” is an additional analytics view not represented as a distinct retained requirement.
- **Candidate:** {'name': 'Generate printable transit labels with barcodes', 'statement': 'The system should generate printable transit labels for items selected for transfer that include a scannable barcode and destination label suitable for affixing to items or containers.', 'priority': 'should', 'category': 'Logistics / Printing'}
  **Sources:** conv_pines018_item_transfer.eml
  **Reason:** Discarded because it is a secondary logistics output not required to satisfy the core transfer management workflow retained in REQ-040 (pull lists) and REQ-037/REQ-041/REQ-042 (movement and reversion).
- **Candidate:** {'name': 'Undo for recent transfers', 'statement': 'The system should provide an undo operation allowing the initiating user or an authorized administrator to revert a completed batch transfer within a configurable time window.', 'priority': 'should', 'category': 'UI / Recovery'}
  **Sources:** conv_pines018_item_transfer.eml
  **Reason:** Discarded as a recovery convenience; audit and scheduled revert are retained (REQ-039, REQ-041/REQ-042). Undo is not necessary for core capability.
- **Candidate:** {'name': 'Option to schedule purging utility', 'statement': 'The system could provide an option to schedule the purging utility or reports to run automatically on a specified cadence.', 'priority': 'could', 'category': 'scheduling'}
  **Sources:** conv_pines021_item_purging.eml
  **Reason:** Discarded because scheduling purging utilities is not needed to satisfy the core purging candidate/reporting and confirmation/audit capabilities retained (REQ-044 through REQ-050).
- **Candidate:** {'name': 'Competing/doubt: automated vs manual cleanup', 'statement': 'There is a competing requirement regarding automation: stakeholders expressed both the desire for an automated/scheduled purging capability and caution that cleanup actions should be manual with confirmation; the decision to automate purge execution versus keeping it manual is unresolved and must be addressed.', 'priority': 'deferred', 'category': 'process-decision'}
  **Sources:** conv_pines021_item_purging.eml
  **Reason:** Discarded because it is an unresolved process decision rather than an implementable atomic capability; the requirements retained enforce safe manual confirmation even if automation is later decided.
- **Candidate:** {'name': 'Display query selections with results', 'statement': 'For every generated report, the system must display the query selection criteria (the filter settings used) alongside or within the report results.', 'priority': 'must', 'category': 'Usability'}
  **Sources:** email_report_features.eml
  **Reason:** Discarded due to scope: the current consolidated set focuses on the specific management-reporting and management-action capabilities represented in the provided candidates for inventory actions and key reports. Displaying query criteria is a cross-cutting reporting UI capability already broadly covered by the reporting architecture in other documentation, but is not included here as a distinct atomic capability to avoid expanding beyond the management-action scope.

## Coverage notes

- This consolidation captures the core management capabilities requested across material volume reporting, capacity dashboards, shelf-space/circulation/collection analysis, missing/damaged and in-transit reporting, item transfer workflow (querying, manual selection, confirmation, audit, and auto-revert), purge/weeding candidate and batch conversion workflows (safe preview and audit), deletion auditing and reporting, patron demographic filtering/reporting, and the inactive patrons report. Several UI/export/secondary enhancements were merged or discarded as they were either implementation detail or subsumed by broader retained capabilities. Deferred/ambiguous items were reduced by selecting best-supported compatible interpretations where possible.
