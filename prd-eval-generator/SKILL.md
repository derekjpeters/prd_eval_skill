---
name: prd-eval-generator
description: Generate golden sets, scoring rubrics, eval schemas, judge prompts, and starter eval runners from a PRD. Use when asked to create evals, golden sets, QA gates, acceptance tests, or model/product evaluation plans from a product requirements document.
---

# PRD Eval Generator

Turn a Product Requirements Document into a practical, PRD-derived evaluation suite: golden set, scoring rubric, deterministic checks, LLM-as-judge prompt, data schema, and a CI-ready runner. Every eval must trace to a specific PRD requirement, metric, guardrail, or risk — never invent evals.

## When to use

Trigger when a user provides a PRD (or points to one) and asks for evals, golden sets, QA gates, acceptance tests, regression gates, or a model/product evaluation plan. Also trigger when someone wants to know "how do we test that this product does what the PRD says."

## Core principles

- **Derive, don't invent.** Every eval maps to a PRD requirement, success metric, guardrail, or named risk. If the PRD is silent on something, mark it `TODO` — do not fabricate.
- **Test the v1 promise.** For v1 products, evaluate the v1 scope, not the long-term vision. Deferred scope becomes preserve-and-flag / negative tests, not feature tests.
- **Separate deterministic from judged.** Anything checkable by code (presence, counts, schema, links, exact values) is a deterministic check. Reserve the LLM judge for genuinely subjective quality.
- **Hard-fail gates for trust/safety.** Safety-critical or trust-critical requirements (e.g. "no silent content loss") are binary gates that fail the case regardless of other scores.
- **Negative tests matter.** Include cases that *should* fail, *should* be flagged, and *should not* be silently accepted. Don't over-index on happy paths.
- **Small and high-signal.** Prefer ~10–20 hand-scored golden cases over hundreds of shallow ones.
- **Regression gates.** Model/prompt changes must not ship unless they pass the golden set at threshold.
- **Judge bias direction.** When safety or trust is involved, the judge should prefer false positives (flagging good output) over false negatives (passing bad output).

## Workflow

1. **Read the PRD carefully.** If it's a file in the repo or provided inline, read the whole thing before extracting.
2. **Extract the product contract** — see the table in section B below. Capture: product goal, target users, primary workflows, functional requirements, non-goals, success metrics, guardrails, quality bars, open questions, known risks, v1 scope, deferred scope.
3. **Convert the contract into eval dimensions.**
4. **Identify hard-fail gates** from safety/trust requirements.
5. **Propose a golden-set sampling plan** covering happy paths, edge cases, deferred/unsupported content, and failure modes.
6. **Define the data** each golden example needs.
7. **Create a weighted scoring rubric** plus hard-fail gates.
8. **Generate deterministic checks** wherever possible.
9. **Generate an LLM-judge prompt** only for subjective checks.
10. **Generate a runner stub** in the project's likely language (see repo inspection below).
11. **Produce a human-review workflow** for hand-scoring and evaluator calibration.
12. **Produce CI / release-gate recommendations.**

## Repo inspection (before writing files)

Inspect the repo first. Reuse existing test/eval conventions, directory layout, and language. Do not introduce a new framework if one already exists.

- TypeScript repo → TypeScript runner and interfaces (explicit types).
- Python repo → Python runner.
- Uncertain → ask, or provide a brief version of both.
- Prefer readable JSON, YAML, and Markdown plus small utilities. Ensure all generated JSON is valid.

## Output sections

Produce these sections in the response, in order:

- **A. Eval Strategy Summary** — what to evaluate and why, in a few sentences.
- **B. PRD-Derived Product Contract** — table: `PRD claim | eval implication | data needed | deterministic or judge | pass/fail criteria`.
- **C. Golden Set Sampling Plan** — per case: `case id | scenario | source requirement | risk covered | data required | expected behavior | hard-fail gate (if any)`.
- **D. Data Schema** — JSON schema for golden cases (see `templates/golden-set-schema.json`).
- **E. Scoring Rubric** — weighted sub-scores + hard-fail gates (see `templates/scoring-rubric-template.md`).
- **F. Deterministic Checks** — assertions implementable without an LLM.
- **G. LLM Judge Prompt** — for subjective checks only (see `templates/llm-judge-prompt-template.md`).
- **H. Eval Runner Stub** — starter code in the repo's language (see `templates/eval-runner-template.ts`).
- **I. Human Scoring Workflow** — how humans label the golden set and calibrate model/evaluator agreement.
- **J. CI / Release Gate** — thresholds that block releases.
- **K. Open Questions** — missing data the PRD does not specify, as `TODO`s.

## Supporting files (progressive disclosure)

Read these only when you reach the relevant step — don't load everything up front:

- `templates/golden-set-schema.json` — schema for a golden case (section D).
- `templates/eval-case-template.json` — a filled generic case with TODO placeholders.
- `templates/scoring-rubric-template.md` — reusable weighted rubric (section E).
- `templates/llm-judge-prompt-template.md` — reusable judge prompt returning structured JSON (section G).
- `templates/eval-runner-template.ts` — starter TypeScript runner (section H).
- `templates/report-template.md` — report format for results.
- `examples/ai-site-migrator-example.md` — a concrete worked example (government site migration, no silent content loss).

## Usage (README)

Point the skill at a PRD and ask for evals:

```
Read docs/prd/site-migrator.md and generate an eval suite.
```

The skill will inspect the repo, extract the product contract, and emit sections A–K plus any files (golden set, runner, rubric) using the templates as scaffolding. Fill each template's `TODO` markers from the PRD; leave genuine gaps as `TODO` in section K rather than inventing values.
