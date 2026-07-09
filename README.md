# prd-eval-skill

A reusable [Claude skill](https://docs.claude.com) that turns a Product Requirements Document into a practical, PRD-derived evaluation suite — golden set, scoring rubric, deterministic checks, an LLM-as-judge prompt, a data schema, and a CI-ready runner — then guides the team through the full eval lifecycle: coverage maps, replay fixtures, calibrated rubrics, experiments, and a disciplined iteration loop.

Every eval traces back to a specific PRD requirement, success metric, guardrail, or risk. The skill does not invent evals, and it marks genuine gaps as `TODO` instead of guessing.

## The five stages

The skill frames every suite within a five-stage maturity model — start at Stage 1, add stages as the system matures:

1. **Golden Sets** — 10–20 hand-scored cases + deterministic checks; baseline correctness, run on every commit.
2. **Labeled Scenarios** — tagged cases + a category × difficulty coverage map; empty cells show where to write tests next.
3. **Replay Harnesses** — real sessions recorded as fixtures; record once, score anytime.
4. **Rubrics** — weighted dimensions with explicit anchors, and an LLM judge calibrated against human scores (correlation ≥ 0.8) before it gates anything.
5. **Experiments** — variant-vs-baseline runs on the same test set, so "is this better?" is answered with data.

After generation it also hands you the operating rhythm: the **iteration loop** (run a pinned baseline → read every failing transcript → diagnose into buckets → fix one bucket with one lever → re-run and ratchet) and a **user-signal intake** map (thumbs-down → rubric case, rephrase → labeled scenario, escalation → golden case, abandoned session → replay fixture).

## What's in here

```
prd-eval-generator/
├── SKILL.md                              # the skill (frontmatter + instructions)
├── templates/
│   ├── golden-set-schema.json            # JSON schema for a golden case
│   ├── eval-case-template.json           # a filled generic case with TODO markers
│   ├── scoring-rubric-template.md        # weighted rubric + hard-fail gates
│   ├── llm-judge-prompt-template.md      # judge prompt returning structured JSON
│   ├── eval-runner-template.ts           # starter TypeScript runner (per-category rollup)
│   ├── eval-runner-template.py           # starter Python runner (per-category rollup)
│   ├── coverage-map-template.md          # category × difficulty coverage matrix
│   ├── iteration-log-template.md         # one-loop record: baseline, buckets, lever, ratchet
│   └── report-template.md                # results report format (categories + failure buckets)
└── examples/
    └── ai-site-migrator-example.md       # worked example (no silent content loss)
```

## Install

The skill lives in the `prd-eval-generator/` folder. Copy that folder into one of these locations:

- **Per project (recommended for teams):** `.claude/skills/prd-eval-generator/` at your repo root, committed to git so everyone on the project gets it.
- **Global (all your projects):** `~/.claude/skills/prd-eval-generator/`.

Claude Code picks it up on the next session — no install command. Verify with `/skills`; you should see `prd-eval-generator` listed.

### Quick install from this repo

```bash
# per-project
git clone https://github.com/derekjpeters/prd_eval_skill.git
mkdir -p your-project/.claude/skills
cp -r prd_eval_skill/prd-eval-generator your-project/.claude/skills/

# or global
mkdir -p ~/.claude/skills
cp -r prd_eval_skill/prd-eval-generator ~/.claude/skills/
```

## Use

Point Claude at a PRD and ask for evals:

```
Read docs/prd/member-concierge.md and generate an eval suite —
golden set, scoring rubric, and a CI gate we can block releases on.
```

Or bring it results and iterate:

```
Our golden set dropped from 87% to 78%. Walk me through one
iteration loop on the failures.
```

The skill inspects the repo, extracts the product contract, and emits an eval strategy plus scaffolded files, reusing your existing test/eval conventions rather than introducing a new framework. It tells you which stage your suite is at and what the next stage adds.

## License

MIT — see [LICENSE](./LICENSE).
