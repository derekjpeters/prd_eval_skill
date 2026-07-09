# Coverage Map — TODO: Product Name (Stage 2: Labeled Scenarios)

Labeled scenarios are golden-set cases with tags. The tags don't change how a test runs — they change what the results tell you. Golden sets answer *"does it work?"*; the coverage map answers *"does it work for all types?"*

Fill each cell with `passed/total` for the cases carrying that label pair. Use `--` for cells with no cases yet.

## Matrix

Rows are `labels.difficulty`, columns are `labels.category` (rename to the product's real categories — e.g. query types, content types, workflows).

| | TODO: category A | TODO: category B | TODO: category C | TODO: category D |
|---|---|---|---|---|
| straightforward | 0/0 | 0/0 | 0/0 | 0/0 |
| ambiguous | 0/0 | -- | 0/0 | -- |
| edge_case | 0/0 | 0/0 | -- | -- |

## How to read it

- **Empty cells (`--`) show where to write tests next.** A missing `edge_case × category D` cell means that combination has never been tested — not that it works.
- **Low cells show where to fix next.** A `1/4` cell is a labeled, countable failure bucket.
- Unlike the golden set, labeled scenarios need **not** all pass — they measure coverage, not release-readiness. Aggregate up, category down: read the breakdown, never just the topline.

## Cadence

- Run labeled scenarios every release (and every iteration loop) — target ~10 minutes.
- Grow from the golden set (10–20 cases) toward 30–100+ labeled cases, sourcing new cases from user sessions and production signals first (`source: user-session | production-signal`).

## TODO ledger

- TODO: categories still unlabeled in the golden set.
- TODO: cells intentionally out of scope for v1 (say why — e.g. deferred scope in the PRD).
