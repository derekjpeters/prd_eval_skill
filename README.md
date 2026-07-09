# prd-eval-skill

A reusable [Claude skill](https://docs.claude.com) that turns a Product Requirements Document into a practical, PRD-derived evaluation suite: golden set, scoring rubric, deterministic checks, an LLM-as-judge prompt, a data schema, and a CI-ready runner.

Every eval traces back to a specific PRD requirement, success metric, guardrail, or risk. The skill does not invent evals, and it marks genuine gaps as `TODO` instead of guessing.

## What's in here

```
prd-eval-generator/
├── SKILL.md                              # the skill (frontmatter + instructions)
├── templates/
│   ├── golden-set-schema.json            # JSON schema for a golden case
│   ├── eval-case-template.json           # a filled generic case with TODO markers
│   ├── scoring-rubric-template.md        # weighted rubric + hard-fail gates
│   ├── llm-judge-prompt-template.md      # judge prompt returning structured JSON
│   ├── eval-runner-template.ts           # starter TypeScript runner
│   ├── eval-runner-template.py           # starter Python runner
│   └── report-template.md                # results report format
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

The skill inspects the repo, extracts the product contract, and emits an eval strategy plus scaffolded files, reusing your existing test/eval conventions rather than introducing a new framework.

## License

MIT — see [LICENSE](./LICENSE).
