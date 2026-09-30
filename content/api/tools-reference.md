---
title: "Tools Reference"
weight: 40
---

The complete catalog of tools exposed by the Teramot MCP server, grouped by domain.
Discover them at runtime with `tools/list`; invoke them with `tools/call`
(see the [Overview](/api/intro/#mcp-methods)).

Most tools accept optional `workspace_name` and `project_name` arguments. When omitted, the
server uses your active context (or the only workspace/project available). If you have multiple
workspaces, name the one you mean.

## Session

| Tool | Description | Parameters |
| --- | --- | --- |
| `switch_context` | Set the default workspace (and optionally project) for the rest of this MCP session. | `workspace_name` (string); `project_name` (string) |

## Workspaces

| Tool | Description | Parameters |
| --- | --- | --- |
| `list_workspaces` | List all workspaces the user has access to. | — |
| `create_workspace` | Create a new workspace. | `name` (string, required); `index_color` (int) |
| `delete_workspace` | Permanently delete a workspace by name. Irreversible; requires owner access. Two-step confirm gate. | `workspace_name` (string, required); `confirmed` (bool) |

## Projects

| Tool | Description | Parameters |
| --- | --- | --- |
| `list_projects` | List projects by name. | `workspace_name` (string) |
| `create_project` | Create a new project inside a workspace. | `workspace_name` (string, required); `slug` (string, required) |
| `delete_project` | Permanently delete a project by name. Irreversible; requires owner access. Two-step confirm gate. | `project_name` (string, required); `workspace_name` (string); `confirmed` (bool) |
| `review_project` | Review a project's overall state: every ETL source and its tables, each table's status and last-refresh date, plus a per-source health summary. | `workspace_name`/`project_name` (string) |

## Project knowledge

| Tool | Description | Parameters |
| --- | --- | --- |
| `project_knowledge` | View a project's durable, shared knowledge document — join keys, business definitions, and caveats about the data (one doc per project, shared by the team). | `workspace_name`/`project_name` (string) |
| `update_project_knowledge` | Create, edit, or delete a project's knowledge document. `create` creates the doc or fully replaces it if one exists; `str_replace` replaces a string that must match exactly once; `insert` adds text after a given line; `delete` removes the doc entirely. | `command` (string, required: create \| str_replace \| insert \| delete); `content` (string, required for create); `old_str`/`new_str` (string, for str_replace); `insert_line` (int, for insert); `insert_text` (string, for insert); `workspace_name`/`project_name` (string) |

## Tables & data

| Tool | Description | Parameters |
| --- | --- | --- |
| `explore_tables` | List or inspect data-warehouse tables. **Listing** (no `table_name`): physical table names, filterable by `layer`; the gold listing also includes results tables still building, failed, or in draft. **Detail** (`table_name` set): one table's SQL, build status, lineage, data-quality profile, and column findings. | `table_name` (string, required for `with_sql`, `with_quality`, `with_status`); `layer` (string: gold \| silver \| bronze); `table_name_filter` (array of string); `with_columns` (bool); `with_instructions` (bool); `with_empty` (bool); `with_sql` (bool); `with_information` (bool); `with_quality` (bool); `with_status` (bool); `with_build_context` (bool); `build_context_table_names` (array of string); `workspace_name`/`project_name` (string) |
| `preview_table` | Preview the first 100 rows of a table (columns, types, sample rows). | `table_name` (string, required); `workspace_name`/`project_name` (string) |
| `query_data` | Execute a SQL query (TRINO dialect) against a table. | `table_name` (string, required); `sql` (string, required); `execution_id` (string); `page` (int); `workspace_name`/`project_name` (string) |
| `revise_silver_query` | Fix a bug in a Silver-layer (processed) table's transformation SQL identified during the conversation. Silver-layer only. Validates first; applying requires explicit user confirmation unless validation is clean and confidence is high. | `table_name` (string, required); `new_sql` (string, required); `reasoning` (string, required); `confidence` (string, required: high \| low); `validate_only` (bool); `confirmed` (bool); `workspace_name`/`project_name` (string) |

## Results (gold) tables

| Tool | Description | Parameters |
| --- | --- | --- |
| `sql_tool` | Run one candidate results-table query and see what it produces — rows, column types, or the engine's error — without creating anything. When the result is right, hand the same SQL to `create_gold_table`. | `query` (string, required); `workspace_name`/`project_name` (string) |
| `create_gold_table` | Create a results table from a SQL definition, used verbatim. On success it submits the build and returns immediately. | `sql` (string, required); `source_tables` (string, required); `name` (string); `description` (string); `questions` (string); `knowledges` (string); `join_keys` (string); `validate_only` (bool); `workspace_name`/`project_name` (string) |
| `update_gold_table` | Update an existing results table: description, instructions, query regeneration, or source tables. | `analysis_spec_name` (string, required); `action` (string: update_description \| create_instruction \| update_instruction \| replace_instruction \| delete_instruction \| regenerate_query); `description` (string); `instructions` (array of `{id?, text}`); `instruction_ids` (array of string); `add_source_tables` (string); `remove_source_tables` (string); `workspace_name`/`project_name` (string) |
| `delete_gold_table` | Permanently delete a results table and all its data. Two-step confirm gate. | `analysis_spec_name` (string); `confirmed` (bool); `workspace_name`/`project_name` (string) |
| `duplicate_gold_table` | Duplicate a results table into a new draft analysis spec. | `analysis_spec_name` (string, required); `dry_run` (bool); `workspace_name`/`project_name` (string) |
| `get_gold_table_download_link` | Get a download link for a results table's full data as a CSV file. Link expires shortly after being issued. | `analysis_spec_name` (string); `visibility` (string: private \| public); `workspace_name`/`project_name` (string) |

## Dashboards

LLM-authored HTML/widget dashboards, each tied to one or more results tables by slug. **Dynamic**
dashboards pair a template with a `query` so data refreshes live; **static** ones have no
`{{expressions}}` and no query.

| Tool | Description | Parameters |
| --- | --- | --- |
| `dashboard_authoring_guide` | The complete guide to writing a dashboard: rendering, the template engine, query rules, widget types, theme, layout, the pre-save checklist, and a worked example. | — |
| `list_dashboards` | List the project's saved dashboards — id, title, type and timestamps, without the document body. | `workspace_name`/`project_name` (string) |
| `get_dashboard` | Retrieve one saved dashboard in full, including its document and query. | `dashboard_id` (string, required); `workspace_name`/`project_name` (string) |
| `preview_dashboard` | Render a dashboard preview in the chat without persisting anything. | `title` (string); `type` (string: html \| widget); `content` (string); `source_html` (string); `query` (string, required if `content` contains `{{expressions}}`); `workspace_name`/`project_name` (string) |
| `save_dashboard` | Persist a new dashboard, wired to one or more results tables by slug. | `title` (string, required); `type` (string: html \| widget, required); `content` (string, required); `source_html` (string); `query` (string); `gold_table_slug` (string); `gold_table_slugs` (array of string, required unless `gold_table_slug` is set); `min_role` (string: readonly \| member \| admin \| owner); `workspace_name`/`project_name` (string) |
| `update_dashboard` | Change a saved dashboard's title, content, query, sources and/or minimum viewing role. Replaces the stored value outright — send complete content, not a fragment. | `dashboard_id` (string, required); `title`/`content`/`source_html`/`query`/`min_role` (string, all optional); `gold_table_slug` (string); `gold_table_slugs` (array of string); `workspace_name`/`project_name` (string) |
| `delete_dashboard` | Delete a saved dashboard. Soft-deleted on the backend but not undoable from this surface, and anyone it was shared with loses access. | `dashboard_id` (string, required); `workspace_name`/`project_name` (string) |

## Refresh & scheduling

| Tool | Description | Parameters |
| --- | --- | --- |
| `refresh_tables` | Trigger an ETL refresh — one table's pipeline or the whole project — to pick up new source data (produces a new revision). | `action` (string, required: refresh_table \| refresh_all); `table_name` (string); `workspace_name`/`project_name` (string) |

## Controls

A control is a business question the team confirmed was answered correctly; the monitor re-asks
it on a cadence and reports whether the answer still arrives the same way.

| Tool | Description | Parameters |
| --- | --- | --- |
| `list_controls` | List the questions a workspace watches month to month — each with its status, the conversation it came from, and when it is due to be re-examined. | `workspace_name` (string) |
| `control_index` | Read one month's decay index for a workspace: the score, its coverage, and any controls it could not judge (flagged insufficient below 50% coverage). | `month` (string, required, YYYY-MM); `workspace_name` (string) |
| `get_control` | Retrieve one control in full: its question, status, who confirmed it, and when it is next due for review. | `control_id` (string, required); `workspace_name` (string) |
| `add_control` | Start watching a question the workspace has already answered correctly. Created as a candidate — not watched until confirmed. | `question` (string, required); `conversation_id` (string, required); `review_due` (string, required, YYYY-MM-DD); `workspace_name` (string) |
| `confirm_control` | Promote a candidate to a watched control, vouching that its answer was right. | `control_id` (string, required); `workspace_name` (string) |
| `remove_control` | Stop watching a question, with a reason. Kept and marked removed, not deleted, so past months still add up. | `control_id` (string, required); `reason` (string, required); `workspace_name` (string) |
