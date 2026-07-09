# Scoring Rubric — TODO: Product Name

The overall score is a weighted sum of dimension sub-scores in `[0, 1]`. **Hard-fail gates override the score**: if any gate triggers, the case fails regardless of the weighted total.

```
overallScore = Σ (dimensionScore_i × weight_i)     # weights sum to 1.0
passed       = overallScore >= PASS_THRESHOLD && no hardFailGate triggered
```

Set `PASS_THRESHOLD` from the PRD's quality bar (default 0.85 when unspecified — mark as TODO if you're guessing).

## Dimensions

Repeat this block per dimension. Weights across all dimensions must sum to 1.0.

### Dimension: TODO: name (weight: TODO: e.g. 0.30)

**What it measures:** TODO: one sentence tied to a PRD requirement/metric.

**Score anchors** (every score point needs an explicit, concrete anchor — a scorer that interprets `0.5` differently each run is useless):
- `1.0` — TODO: what full credit looks like, concretely (e.g. "all facts correct and verifiable from cited sources").
- `0.5` — TODO: what partial credit looks like (e.g. "mostly correct with one minor inaccuracy").
- `0.0` — TODO: what failure looks like (e.g. "contains significant errors or fabricated information").

**Full credit example:** TODO
**Partial credit example:** TODO
**Failure example:** TODO

## Hard-fail gates

List each binary gate. A single triggered gate fails the case.

- **TODO-GATE-ID** — TODO: description. Triggers when: TODO condition. Source: TODO PRD guardrail/risk.

## Score thresholds → action

Map overall-score bands to actions so a number is never the end of the conversation (adjust bands to the PRD's quality bar):

| Overall score | Quality | Action |
|---|---|---|
| 0.90–1.00 | Excellent | Ship it |
| 0.70–0.89 | Good | Minor tweaks |
| 0.50–0.69 | Acceptable | Review and improve |
| 0.30–0.49 | Poor | Significant work needed |
| < 0.30 | Critical | Stop. Fix now. |

## Notes

- Every dimension must trace to a PRD claim, metric, guardrail, or risk. If it doesn't, remove it.
- Prefer deterministic checks for anything mechanically verifiable; reserve judged dimensions for genuine subjectivity.
- Make every criterion falsifiable: it is done when you can write one example that unambiguously passes and one that unambiguously fails. Length, tone, and bare scale labels are proxies for quality — describe the quality itself.
- Before an LLM judge gates anything with this rubric, calibrate it: hand-score ~20 real outputs, run the judge on the same outputs, and check correlation (target ≥ 0.8). If it's lower, fix the rubric anchors — a judge with a bad rubric produces confident, wrong scores.
