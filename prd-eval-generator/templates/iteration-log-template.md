# Iteration Log — TODO: Product Name, Loop TODO-N

One loop = one change, verified. Then go again. Fill one copy of this file per loop.

## 1. Pinned baseline (Run)

Pin everything before you touch anything — an unpinned baseline means the re-run can't attribute the change (your fix vs. drift).

| Pin | Value |
|---|---|
| Golden set / dataset version | TODO (frozen, e.g. `golden-v12`) |
| Model | TODO (pinned version) |
| Prompt version | TODO (file + commit, e.g. `prompts/support@a41f3c`) |
| Tool definitions version | TODO |

**Baseline result:** pass TODO% · rubric TODO/5 · cost TODO/case · runtime TODO

## 2. Read every failing transcript (Read)

Read the full trajectory, not just the final answer — agents fail in the middle. For each failure, mark the **first wrong step** (everything after it is noise) and write **one line** on what went wrong, in plain words. Thirty failures is an hour of reading; do it before every fix.

| Case ID | First wrong step | One-line diagnosis |
|---|---|---|
| TODO | TODO | TODO |

## 3. Group failures into a taxonomy (Diagnose)

Labels come from reading, not guessing. Five buckets, not fifteen.

| Bucket | Count | Example |
|---|---|---|
| TODO (e.g. wrong tool selected) | 0 | TODO |
| TODO (e.g. retrieval miss) | 0 | TODO |
| TODO (e.g. hallucinated fact) | 0 | TODO |

## 4. Fix the biggest bucket with ONE lever (Fix)

Biggest bucket first — with one exception: safety and trust failures jump the queue, whatever their count. One bucket per loop, one lever per loop, so the re-run tells you if the fix worked. Write the fix from the transcripts ("For policy questions, call kb.policy; never web.search for internal docs"), not as a wish ("be more careful choosing tools").

Levers, ordered by cost — exhaust the cheap ones first:

| # | Lever | Cost | Typically fixes |
|---|---|---|---|
| 1 | Prompt & instructions | minutes | most buckets start here |
| 2 | Tool definitions & descriptions | hours | wrong-tool, bad-args |
| 3 | Retrieval & context | days | retrieval-miss |
| 4 | Model or architecture | weeks | only when 1–3 are exhausted |

**Bucket chosen:** TODO · **Lever pulled:** TODO · **Exact change:** TODO

## 5. Re-run against the baseline (Re-run)

Same pins, one change. Aggregate up, category down — read the breakdown, never just the topline; a fix can break something else.

| Category | Before | After | Note |
|---|---|---|---|
| TODO | 0/0 | 0/0 | the fix, working / unaffected / regression — caught pre-ship |

## 6. Ratchet decision

- [ ] The fix ships with the test case that proves its bucket is fixed.
- [ ] Baseline moves only on a full-suite pass — the bar can only go up.
- [ ] No category ships below its previous score (categories are the ratchet, not the average).
- [ ] No test was removed or expected output edited just to make the run green — never.

**Decision:** TODO ratchet forward to `golden-vN+1` / hold baseline · **Next loop:** TODO bucket, TODO lever
