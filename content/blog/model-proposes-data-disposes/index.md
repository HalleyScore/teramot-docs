---
title: "The Model Proposes, the Data Disposes"
date: 2026-10-22T09:00:00-03:00
draft: false
authors:
  - valentin-torassa
tags:
  - ai
  - architecture
  - mcp
  - data-quality
  - product-engineering
categories:
  - engineering
summary: "If you can connect Claude to a database in an afternoon, what is Teramot for? Everywhere a model touches our platform it only proposes: code measures the proposal against the real data, and a fixed rule decides. Eleven figures, every number from the code."
showTableOfContents: true
---

{{< intro >}}
If you can connect Claude to a database in an afternoon, what is Teramot for? Everywhere a model touches Teramot, it only proposes. Code measures the proposal against the real data, within a fixed number of tries, and a fixed rule decides what ships. This post walks through where that happens, with the code behind every number. It is also why the model is the part we can swap.
{{< /intro >}}

The afternoon is real. Claude writes good SQL, and wiring it to a database is a small job. This post is about the day after.

{{< stats columns="4" >}}
{{< stat value="0" label="Model calls in the MCP server" >}}The server has no LLM SDK. Its checks are plain Go.{{< /stat >}}
{{< stat value="60" label="Typed tools" >}}Where a pipe has one: `execute_sql`.{{< /stat >}}
{{< stat value="13,388" label="Automated tests" >}}Across the platform, Beacon, Lambda, Fingerprint and Spectra, counted on 20 October 2026.{{< /stat >}}
{{< stat value="17" label="Source types" >}}From SAP to Google Sheets.{{< /stat >}}
{{< /stats >}}

## 1. Claude plus a connection string

The pipe has one verb. The model writes SQL, the database runs it with whatever the role allows, and nothing records how the number was made. On a demo schema that works. On real company data it fails quietly: the query runs, the number looks plausible, and it is wrong.

{{< inlinesvg src="svg/model-proposes/pipe.svg" caption="Same model in both rows. The difference is everything to its right." >}}

Four of those quiet failures happened to us. None of them raised an error.

{{< inlinesvg src="svg/model-proposes/incidents.svg" caption="Each number comes from the code comment or test fixture that records it. The fourth is a client's case, anonymized." >}}

Each one is now a mechanism, and every mechanism has the same shape.

## 2. Propose, measure, decide

Teramot has one algorithm. The model proposes something: a cleaning query, a type fix, a plan for which rows to pull, a paragraph of a report. Teramot measures the proposal against the real data, with a dry run, an `EXPLAIN`, a `COUNT` or a probe join. Then a fixed rule decides. A failed proposal goes back to the model with the engine's error and the numbers we measured, and the model tries again. When the tries run out, a safe default ships. For a cleaning query that default is a plain copy of the table, never the model's last guess.

{{< inlinesvg src="svg/model-proposes/loop.svg" caption="A failed proposal goes back with the evidence. The model never decides whether its own work ships." >}}

Why not write the rule in the prompt? We did. The cleaning agent's prompt says plainly that a key column must not change. In a calibration run of 14 cases, the production model reshaped a named key in 4 of them anyway. The design doc for that stage puts it better than I can: a section that states a rule gets "usually"; a guard gets "never".

{{< inlinesvg src="svg/model-proposes/trace.svg" caption="The rules are the real ones. This stage exists because a `CAST` once turned a 25-digit account number into a different number." >}}

The guard does not judge style. It parses the final query and checks two things: that no outer clause can drop rows, and that every key column still holds the same value. `TRIM` and `NULLIF(x, '')` pass, because every model reaches for them and neither changes a real value. A `CAST`, a `lower()` or a `COALESCE` on a key fails, because the join downstream would compare something else.

The same loop runs in six places.

{{< inlinesvg src="svg/model-proposes/where.svg" caption="What the model proposes, how Teramot checks it, and the gate that decides. For join keys, measuring beat the model, so the model is gone from that step." >}}

## 3. Before the question

Most of the work happens before anyone asks anything. Sources are loaded incrementally where they allow it and merged on their keys. Each table is profiled across all its rows, not a sample, so the cleaning agent starts from the table's real null rates and cardinalities. Types are reconciled across tables. Column lineage is parsed from the SQL, not described by a model. When a source changes, the changed tables are audited again, a write gate runs `EXPLAIN` before anything destructive, and results tables that broke are marked outdated, with a repair that waits for a person to approve it.

{{< inlinesvg src="svg/model-proposes/pipeline.svg" caption="The strip is the whole pipeline in order: nine steps of code, five checked proposals, one human decision." >}}

The write gate comes from the 40-day incident. A silver table is rebuilt in two steps, a `DELETE` and then an `INSERT`, with no transaction between them. When a type changed upstream, the delete committed, the insert failed, and the scheduled refresh repeated that every day. `EXPLAIN` plans a write without running it, so now a write that cannot succeed is known before anything is deleted.

Join keys are the step where we removed the model. The old detector proposed keys from column names and a cardinality check, and never looked at the values. Measured, about 77% of the edges it had stored in production failed validation. Since August 2026 the platform builds an index of distinct values and runs one verifying join per candidate. An edge is accepted only if at least 95% of rows find a match, at least 90% of the distinct values are contained, and the referenced side is really unique. Two parallel tables that contain each other almost completely are rejected: they are siblings, not a key and its parent.

{{< inlinesvg src="svg/model-proposes/fk.svg" caption="The old detector guessed from names. Since August 2026 every candidate is verified with a real join." >}}

The model did not get worse at this. Counting was never a language problem.

## 4. During the question

Here is one question from Claude, through our MCP server. Claude signs in as the user, not as a service account. It asks for the project's tables and gets them under aliases, with the project's business rules attached: the definitions the team wrote down, such as what counts as revenue. Then it writes SQL.

{{< inlinesvg src="svg/model-proposes/lanes.svg" caption="The model never holds credentials or physical table names, and the MCP server never calls a model." >}}

From there everything is code. The MCP server refuses `SELECT *` and caps the answer at 500 rows and 45 seconds, because MCP clients give up at 60. The backend parses the query into exactly one read-only statement and checks on the syntax tree that it touches only this project's tables. If Athena rejects it, the engine's error comes back rewritten as a fix the model can act on. The backend records the path the query took. Physical names become aliases on the way out, and the business rules travel back with the rows. Claude writes the answer.

## 5. After the answer

An answer that was right last month can be wrong tonight and still look like an answer. A source changes, a key drifts, a join that matched everything yesterday matches a third of it today. Comparing numbers cannot catch this, because numbers move for real reasons too. A smaller revenue figure might just be a bad month.

So each query leaves a fingerprint: the tables it read, each join with its measured match rate, the columns it used and the order of magnitude of the rows. Never a value. When a person confirms that a question is worth watching, Lambda can ask it again and compare the new path with the confirmed one, using fixed rules and no model.

{{< inlinesvg src="svg/model-proposes/path.svg" caption="Numbers move for real reasons. Paths shouldn't." >}}

The 1.1 million tonnes from the first section are the case those rules are tested against. A written instruction told the system to join two tables on the wrong key. The join matched nothing, every derived column came back zero, and the answer reported those zeros confidently for about two months. The test fixture says it best: obeying an instruction that is wrong about the data is indistinguishable from obeying a right one, unless something measures the join. A join that falls to 0% now reads as `broken`.

## 6. Swap the model

Because the checks live outside the model, changing the model is configuration. On 28 September 2026 Beacon's default moved from Claude Sonnet 5 to GPT-6 Luna. On our funnel benchmark Luna answered 95.2% correctly against Sonnet's 100%, the two were equal on the assistant A/B, and Luna runs at about a twenty-fifth of the list price. Going back is one environment variable.

{{< inlinesvg src="svg/model-proposes/swap.svg" caption="Beacon's default model changed on 28 September 2026. Nothing else did." >}}

On the platform each agent's model is a feature flag, and an agent can name a fallback provider for outages. Which model is best this quarter is a question we get to keep asking.

## 7. The job, not the tool

Foundation Capital has a name for where this goes: [service as software](https://foundationcapital.com/ideas/ai-leads-a-service-as-software-paradigm-shift). Software as a service sells you a tool and leaves the job to your team. Service as software does the job, and the company selling it is responsible for the outcome.

That second sentence is the argument of this whole post. You can only be responsible for a result you measured. A pipe to a model cannot take the job, because nothing in it can tell a right number from a confident one. The loop is what lets Teramot take the job instead of selling the tool.

{{< inlinesvg src="svg/model-proposes/job.svg" caption="In SaaS a person does six of these jobs and nobody does the seventh. In Teramot a person steps in on two, only to decide." >}}

People stay where judgment lives: approving a repair after a source changes, and choosing which answers are worth watching. Everything else is a mechanism with a test.

Bruno Ruyú made the business case in [Trivial](https://teramot.com/blog/trivial): a frontier model with your documents is a weekend project, and what compounds is everything around it. This post is the engineering side, and Sol's [post on Beacon's cache](/blog/eight-rows-not-twelve-million/) goes deep on one piece of it. The model proposes. The data disposes.

*— Valentín Torassa*
