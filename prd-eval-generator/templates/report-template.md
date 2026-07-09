# Eval Report — TODO: Product / Run Label

**Run date:** TODO
**Commit / model / prompt version:** TODO
**Golden set version:** TODO

## Summary

TODO: 2–3 sentences on overall health and whether this run should ship.

## Pass rate

| Metric | Value |
|---|---|
| Total cases | TODO |
| Passed | TODO |
| Failed | TODO |
| Pass rate | TODO% |
| Release threshold | TODO% |

## Hard failures

List every case that triggered a hard-fail gate. Any hard failure blocks release.

- **TODO-CASE-ID** — gate `TODO-GATE-ID`: TODO what happened.
- _None_ if clean.

## Per-case results

| Case ID | Name | Score | Passed | Hard-fail | Notes |
|---|---|---|---|---|---|
| TODO | TODO | 0.00 | ✅/❌ | yes/no | TODO |

## Evaluator / human agreement

How closely the automated evaluator matched hand-scored reference labels.

| Metric | Value |
|---|---|
| Cases with human label | TODO |
| Mean abs. score delta (human vs evaluator) | TODO |
| Gate agreement (human vs evaluator) | TODO% |

If agreement is low, recalibrate the rubric or judge prompt before trusting the gate.

## Recommended fixes

- TODO: highest-signal issues to fix, ordered by impact.

## Release recommendation

**TODO: SHIP / BLOCK** — TODO one-line rationale (e.g. "BLOCK: 2 hard failures on silent content loss").
