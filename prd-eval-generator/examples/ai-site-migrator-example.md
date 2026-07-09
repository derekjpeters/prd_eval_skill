# Worked Example — AI Site Migrator

A concrete application of the skill. The product migrates government websites into native, editable pages. The overriding promise is **zero silent content loss**: nothing may disappear without being either migrated or explicitly flagged. Pages are scored against their source, using a golden set of ~15 hand-scored real pages. In v1, forms, calendars, meetings, and listings are **preserve-and-flag** cases, not full-fidelity conversions.

## A. Eval Strategy Summary

Evaluate whether each migrated page faithfully reproduces its source page's content, links, and assets, and whether anything the v1 migrator can't natively convert is preserved and flagged rather than dropped. The single non-negotiable is no silent loss of content, links, images, documents, or unsupported blocks. Quality dimensions (section fit, metadata) are scored; loss is a hard-fail gate.

## B. PRD-Derived Product Contract (excerpt)

| PRD claim | Eval implication | Data needed | Deterministic / judge | Pass/fail criteria |
|---|---|---|---|---|
| No silent content loss | Every source block appears migrated or flagged | Source DOM inventory, output inventory | Deterministic | Any unaccounted block → hard fail |
| Pages migrate to native editable pages | Output uses native components, not iframes/screenshots | Output structure | Deterministic | Non-native embed of supported content → fail |
| Forms preserved & flagged in v1 | Forms not silently dropped or half-converted | Source forms, output flags | Deterministic | Missing form or missing flag → hard fail |
| Faithful to source | Content reads/represents the same | Source text, output text | Judge | Meaning preserved, no fabrication |
| Links correct | All source links resolve to correct targets | Source links, output links | Deterministic | Broken/wrong/missing link → fail dimension |

## C. Golden Set Sampling Plan — 15 case categories

| # | Case category | Source requirement | Risk covered | Hard-fail gate |
|---|---|---|---|---|
| 1 | Simple text/content page | Faithful migration | Baseline content loss | Silent content loss |
| 2 | Page with many internal links | Link correctness | Broken navigation | — |
| 3 | Page with external + mailto/tel links | Link correctness | Dropped contact links | — |
| 4 | Page with embedded images | Asset preservation | Missing images | Silent asset loss |
| 5 | Page linking PDFs / documents | Document preservation | Lost official documents | Silent document loss |
| 6 | Page with an online form | Preserve-and-flag (v1) | Silent form loss | Form dropped or unflagged |
| 7 | Page with an events calendar | Preserve-and-flag (v1) | Silent calendar loss | Calendar dropped or unflagged |
| 8 | Page with a meetings/agenda module | Preserve-and-flag (v1) | Lost meeting records | Module dropped or unflagged |
| 9 | Page with a directory/listing | Preserve-and-flag (v1) | Lost listings | Listing dropped or unflagged |
| 10 | Page with tables of data | Structure/metadata | Mangled tables | Silent row/cell loss |
| 11 | Page with nested sections/accordions | Section fit | Collapsed/lost sections | Silent section loss |
| 12 | Page mixing supported + unsupported blocks | Unsupported handling | Partial silent drop | Any unflagged unsupported block |
| 13 | Page with iframes/third-party embeds | Unsupported handling | Silent embed loss | Embed dropped or unflagged |
| 14 | Page with rich metadata (SEO, breadcrumbs) | Metadata/structure | Lost metadata | — |
| 15 | Long, deeply nested page | Content completeness at scale | Truncation/omission | Silent content loss |

Each becomes a `GoldenCase` (see `../templates/golden-set-schema.json`) with a real source snapshot, an expected inventory, and expected flags for preserve-and-flag categories.

## D/E. Scoring Dimensions

| Dimension | Weight | Judge/Deterministic |
|---|---|---|
| Content completeness | 0.30 | Deterministic (inventory diff) + judge for meaning |
| Link correctness | 0.20 | Deterministic |
| Asset / document preservation | 0.20 | Deterministic |
| Section fit | 0.10 | Judge |
| Unsupported content handling | 0.15 | Deterministic (flag presence) |
| Metadata / structure | 0.05 | Deterministic |

Weights sum to 1.0.

### Hard-fail gate

> No content, link, image, document, or unsupported block may disappear without being migrated or flagged. Any such silent loss fails the case regardless of the weighted score.

## H. Sample TypeScript scoring function

```typescript
interface MigrationScore {
  overallScore: number;      // weighted sum of the six dimensions, [0,1]
  silentContentLoss: boolean; // true if any block vanished without migration or flag
}

function migrationCasePassed(score: MigrationScore): boolean {
  const passed = score.overallScore >= 0.85 && !score.silentContentLoss;
  return passed;
}
```

## J. CI / Release Gate

- **Block release** if any case has `silentContentLoss === true`.
- **Block release** if pass rate across the 15 golden cases falls below 90%.
- Regression gate: a new model/prompt must meet or beat the current golden-set pass rate and introduce zero new hard failures.

## K. Open Questions (example TODOs)

- TODO: Exact definition of a "block" for inventory diffing (DOM node vs semantic unit)?
- TODO: Are historical calendar/meeting entries in scope for preservation, or only current?
- TODO: Threshold for "faithful" text on the judge dimension — paraphrase tolerated or verbatim required?
