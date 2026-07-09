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

**Scoring guidance:**
- `1.0` — TODO: what full credit looks like.
- `0.5` — TODO: what partial credit looks like.
- `0.0` — TODO: what failure looks like.

**Full credit example:** TODO
**Partial credit example:** TODO
**Failure example:** TODO

## Hard-fail gates

List each binary gate. A single triggered gate fails the case.

- **TODO-GATE-ID** — TODO: description. Triggers when: TODO condition. Source: TODO PRD guardrail/risk.

## Notes

- Every dimension must trace to a PRD claim, metric, guardrail, or risk. If it doesn't, remove it.
- Prefer deterministic checks for anything mechanically verifiable; reserve judged dimensions for genuine subjectivity.
