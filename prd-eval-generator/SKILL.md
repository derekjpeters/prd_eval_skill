---
name: prd-eval-generator
description: Generate golden sets, scoring rubrics, eval schemas, judge prompts, and starter eval runners from a PRD, then guide the full eval lifecycle — labeled scenarios and coverage maps, replay fixtures, calibrated rubrics, experiments, and the run→read→diagnose→fix→re-run iteration loop. Use when asked to create evals, golden sets, QA gates, acceptance tests, or evaluation plans from a product requirements document, or to iterate on and mature an existing eval suite.
---

# PRD Eval Generator

Turn a Product Requirements Document into a practical, PRD-derived evaluation suite: golden set, scoring rubric, deterministic checks, LLM-as-judge prompt, data schema, and a CI-ready runner. Every eval must trace to a specific PRD requirement, metric, guardrail, or risk — never invent evals.

The suite is stage 1 of a five-stage eval program (see the maturity model below). Beyond generating artifacts, guide the user through the stages: where they are, what the next stage adds, and how to run the iteration loop once results exist.

## When to use

Trigger when a user provides a PRD (or points to one) and asks for evals, golden sets, QA gates, acceptance tests, regression gates, or a model/product evaluation plan. Also trigger when someone wants to know "how do we test that this product does what the PRD says," when they have eval results and ask what to fix next, or when they want to grow an existing suite (coverage, replay, rubrics, experiments).

## Core principles

- **Derive, don't invent.** Every eval maps to a PRD requirement, success metric, guardrail, or named risk. If the PRD is silent on something, mark it `TODO` — do not fabricate.
- **Test the v1 promise.** For v1 products, evaluate the v1 scope, not the long-term vision. Deferred scope becomes preserve-and-flag / negative tests, not feature tests.
- **Separate deterministic from judged.** Anything checkable by code (presence, counts, schema, links, exact values) is a deterministic check. Reserve the LLM judge for genuinely subjective quality.
- **Hard-fail gates for trust/safety.** Safety-critical or trust-critical requirements (e.g. "no silent content loss") are binary gates that fail the case regardless of other scores.
- **Negative tests matter.** Include cases that *should* fail, *should* be flagged, and *should not* be silently accepted. Don't over-index on happy paths.
- **Small and high-signal.** Prefer ~10–20 hand-scored golden cases over hundreds of shallow ones.
- **Regression gates.** Model/prompt changes must not ship unless they pass the golden set at threshold.
- **Judge bias direction.** When safety or trust is involved, the judge should prefer false positives (flagging good output) over false negatives (passing bad output).
- **Falsifiable criteria only.** A criterion is done when you can write one concrete example that unambiguously passes and one that unambiguously fails. Length, tone, and bare scale labels are proxies for quality — describe the quality itself.
- **Real signal beats synthetic.** Source cases from user sessions and production signals wherever they exist; real phrasing is messier than anything you'd write yourself, and that's the point.
- **Score trajectories for agents.** Agent products fail in the middle, not just at the end. Check tool choice, arguments, and call order deterministically; judge step reasonableness only where genuinely subjective.

## Five-stage maturity model

Frame every suite within these five stages (each builds on the last). Start at Stage 1; add stages as the system matures. Always state which stage the generated suite puts the team at and what the next stage would add.

| Stage | What it adds | Core artifact | Run cadence | Output sections |
|---|---|---|---|---|
| 1. Golden Sets | Baseline correctness | 10–20 hand-scored cases + deterministic checks | Every commit (~1 min) | C, D, F, H |
| 2. Labeled Scenarios | Coverage mapping | Tagged cases (30–100+) + coverage matrix | Every release / every loop (~10 min) | L |
| 3. Replay Harnesses | Reproducibility + metrics | Recorded session fixtures, re-scoreable anytime | Weekly / before merging (~1 hr) | H, M |
| 4. Rubrics | Multi-dimensional quality | Anchored weighted rubric + calibrated LLM judge | Before shipping | E, G, I |
| 5. Experiments | Decisions with data | Variant-vs-baseline runs on the same test set | Before shipping any change | N |

Golden sets answer "does it work?"; labeled scenarios answer "does it work for all types?". Golden cases must all pass; labeled scenarios need not. The earlier a regression is caught, the cheaper it is to fix.

## Workflow

1. **Read the PRD carefully.** If it's a file in the repo or provided inline, read the whole thing before extracting.
2. **Extract the product contract** — see the table in section B below. Capture: product goal, target users, primary workflows, functional requirements, non-goals, success metrics, guardrails, quality bars, open questions, known risks, v1 scope, deferred scope.
3. **Convert the contract into eval dimensions.**
4. **Identify hard-fail gates** from safety/trust requirements.
5. **Propose a golden-set sampling plan** covering happy paths, edge cases, deferred/unsupported content, and failure modes.
   - *Concrete vs. parameterized:* when the PRD fixes the product's behavior, write concrete cases with real inputs and expected outputs, ready to score. When the behavior is chosen by the end user (e.g. a "pick your own behavior" assignment), the golden set is role-defined scaffolding — define each case's role, scenario shape, and pass criteria, and let the user instantiate the specifics once they've picked the behavior. State explicitly which mode the golden set is in.
   - *Label and source every case:* tag each case with `labels` (category, subcategory, difficulty) and a `source` (prd | user-session | production-signal | synthetic). Labels don't change how a case runs — they change what the results tell you.
6. **Define the data** each golden example needs.
7. **Create a weighted scoring rubric** plus hard-fail gates, with an explicit anchor for every score point.
8. **Generate deterministic checks** wherever possible.
9. **Generate an LLM-judge prompt** only for subjective checks, with a calibration plan (judge vs. human agreement) before it's trusted.
10. **Generate a runner stub** in the project's likely language (see repo inspection below).
11. **Produce a human-review workflow** for hand-scoring and evaluator calibration.
12. **Produce CI / release-gate recommendations.**
13. **Produce a coverage map** once cases are labeled — the category × difficulty matrix that shows where to write tests next.
14. **Produce an iteration playbook** — the loop the team runs when results come back: pinned baseline, error analysis into buckets, one lever per loop, ratchet rules.
15. **Produce a user-signal intake plan** — how user testing and production signals become new eval cases over time.

## Repo inspection (before writing files)

Inspect the repo first. Reuse existing test/eval conventions, directory layout, and language. Do not introduce a new framework if one already exists.

- TypeScript repo → TypeScript runner and interfaces (explicit types); start from `templates/eval-runner-template.ts`.
- Python repo → Python runner; start from `templates/eval-runner-template.py`.
- Uncertain → ask, or provide a brief version of both.
- Prefer readable JSON, YAML, and Markdown plus small utilities. Ensure all generated JSON is valid.

## Output sections

Produce these sections in the response, in order:

- **A. Eval Strategy Summary** — what to evaluate and why, in a few sentences.
- **B. PRD-Derived Product Contract** — table: `PRD claim | eval implication | data needed | deterministic or judge | pass/fail criteria`.
- **C. Golden Set Sampling Plan** — per case: `case id | scenario | source requirement | risk covered | data required | expected behavior | labels | source | hard-fail gate (if any)`. Keep it 10–20 cases; four check types to draw on: tool selection, source citation, content validation, negative validation.
- **D. Data Schema** — JSON schema for golden cases (see `templates/golden-set-schema.json`).
- **E. Scoring Rubric** — weighted sub-scores + hard-fail gates, every score point anchored with a concrete description, plus score-threshold → action guidance (see `templates/scoring-rubric-template.md`).
- **F. Deterministic Checks** — assertions implementable without an LLM. For agent products include tool-call checks (right tool, right args, right order, forbidden tools) and efficiency checks (steps to completion, redundant calls, loop detection) — trajectories that pass end-to-end can still burn 3× the tokens.
- **G. LLM Judge Prompt** — for subjective checks only, calibrated against ~20 hand-scored examples (target correlation ≥ 0.8) before it gates anything (see `templates/llm-judge-prompt-template.md`).
- **H. Eval Runner Stub** — starter code in the repo's language (see `templates/eval-runner-template.ts` for TypeScript projects, `templates/eval-runner-template.py` for Python projects). Recommend recording real sessions as JSON fixtures — record once, score anytime — so the suite gains replay (Stage 3) without re-paying inference.
- **I. Human Scoring Workflow** — how humans label the golden set and calibrate model/evaluator agreement. If the PRD already describes a standing human-review or transcript-review cadence, map the eval's human scoring onto that existing process — same reviewers, same sessions — rather than proposing a parallel one.
- **J. CI / Release Gate** — thresholds that block releases, matched to cadence: every commit → golden set; every release → labeled scenarios; weekly → replay + deep analysis; before shipping → rubric evals and an experiment validating the change.
- **K. Open Questions** — missing data the PRD does not specify, as `TODO`s.
- **L. Coverage Map** — the Stage-2 instrument: a category × difficulty matrix of `passed/total` across labeled cases. Empty cells show where to write tests next (see `templates/coverage-map-template.md`).
- **M. Iteration Playbook** — the operating rhythm once results exist: pin a baseline (dataset, model, prompt, tools), then run → read every failing transcript → diagnose failures into ≤5 buckets → fix the biggest bucket (safety/trust jumps the queue) with ONE lever → re-run against the baseline. One loop = one change, verified (see `templates/iteration-log-template.md`).
- **N. User-Signal Intake** — how real usage feeds the suite: thumbs-down → rubric case; rephrase/retry → labeled scenario (missed intent); escalation to human → golden case; abandoned session → replay fixture read end-to-end. Every user failure becomes an eval case, annotated with its `source`.

## Anti-patterns (reject these when writing criteria)

All three describe form, not quality:

- **The Likert trap** — "rate 1–5" with undefined points. Two scorers give the same adequate answer a 3 and a 4; aggregated scores become noise. Define every point on the scale — if you can't write the anchor, the quality bar isn't defined yet.
- **Vague criteria** — "demonstrates strategic thinking." Undefined terms make humans disagree and LLM judges hallucinate a definition. Make it falsifiable: "identifies ≥ 2 explicit trade-offs with concrete examples."
- **Ambiguous ranges** — "response between 300 and 500 tokens." A 450-token miss passes; a 250-token perfect answer fails. Describe what good looks like instead: "answers all parts of the question; does not include unrequested information."

## Supporting files (progressive disclosure)

Read these only when you reach the relevant step — don't load everything up front:

- `templates/golden-set-schema.json` — schema for a golden case (section D).
- `templates/eval-case-template.json` — a filled generic case with TODO placeholders.
- `templates/scoring-rubric-template.md` — reusable weighted rubric with anchors (section E).
- `templates/llm-judge-prompt-template.md` — reusable judge prompt returning structured JSON, with calibration guidance (section G).
- `templates/eval-runner-template.ts` — starter TypeScript runner (section H, TypeScript projects).
- `templates/eval-runner-template.py` — starter Python runner (section H, Python projects).
- `templates/coverage-map-template.md` — category × difficulty coverage matrix (section L).
- `templates/iteration-log-template.md` — one-loop iteration record: baseline, buckets, lever, re-run, ratchet (section M).
- `templates/report-template.md` — report format for results, with per-category breakdown and failure buckets.
- `examples/ai-site-migrator-example.md` — a concrete worked example (government site migration, no silent content loss).

## Usage (README)

Point the skill at a PRD and ask for evals:

```
Read docs/prd/site-migrator.md and generate an eval suite.
```

Or bring it results and iterate:

```
Our golden set is at 78% (was 87%). Walk me through one iteration loop on the failures.
```

The skill will inspect the repo, extract the product contract, and emit sections A–N plus any files (golden set, runner, rubric, coverage map, iteration log) using the templates as scaffolding. Fill each template's `TODO` markers from the PRD; leave genuine gaps as `TODO` in section K rather than inventing values. For quick asks, sections A–K are the core deliverable; produce L–N when the user wants coverage, iteration, or production-feedback guidance — and always say which stage the suite is at.
