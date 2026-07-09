/**
 * Starter eval runner. Replace the placeholder functions
 * (`runSystemUnderTest`, `callLlmJudge`) with real implementations.
 *
 * Usage:
 *   ts-node eval-runner-template.ts ./golden/*.json
 *   (or wire into your existing test command / CI job)
 */

// ---------- Types ----------

export interface HardFailGate {
  id: string;
  description: string;
}

export interface GoldenCase {
  id: string;
  name: string;
  prdRequirementIds: string[];
  scenario: string;
  userPersona?: string;
  input: unknown;
  expectedOutput: unknown;
  expectedFlags?: string[];
  expectedArtifacts?: string[];
  hardFailGates?: HardFailGate[];
  scoringWeights?: Record<string, number>;
  labels?: Record<string, string>;
  source?: string;
  humanScore?: number | null;
  notes?: string;
}

export interface DeterministicResult {
  name: string;
  passed: boolean;
  detail?: string;
}

export interface JudgeResult {
  passed: boolean;
  overallScore: number;
  scores: Record<string, number>;
  hardFailTriggered: boolean;
  missingRequirements: string[];
  incorrectClaims: string[];
  notes: string;
}

export interface CaseResult {
  caseId: string;
  name: string;
  passed: boolean;
  overallScore: number;
  hardFailTriggered: boolean;
  deterministic: DeterministicResult[];
  judge?: JudgeResult;
  notes: string;
}

export interface CategoryStats {
  total: number;
  passed: number;
}

export interface RunReport {
  total: number;
  passed: number;
  failed: number;
  passRate: number;
  hardFailures: string[];
  byCategory: Record<string, CategoryStats>;
  results: CaseResult[];
  releaseRecommendation: "SHIP" | "BLOCK";
}

// ---------- Config ----------

const PASS_THRESHOLD = 0.85; // TODO: set from PRD quality bar
const RELEASE_PASS_RATE = 0.9; // TODO: set from CI/release gate policy

// ---------- Placeholders (implement these) ----------

/** Run the product/system under test against a case's input. */
async function runSystemUnderTest(input: unknown): Promise<unknown> {
  // TODO: call the real system.
  throw new Error("runSystemUnderTest not implemented");
}

/** Call the LLM judge for subjective dimensions. Return parsed JSON. */
async function callLlmJudge(
  goldenCase: GoldenCase,
  actualOutput: unknown
): Promise<JudgeResult> {
  // TODO: render the judge prompt template, call the model, parse the JSON.
  throw new Error("callLlmJudge not implemented");
}

// ---------- Deterministic checks ----------

/**
 * Assertions that need no LLM. Extend per product:
 * presence of expected flags, artifacts, exact fields, counts, links, etc.
 */
function runDeterministicChecks(
  goldenCase: GoldenCase,
  actualOutput: unknown
): DeterministicResult[] {
  const results: DeterministicResult[] = [];
  const output = actualOutput as Record<string, unknown>;

  for (const flag of goldenCase.expectedFlags ?? []) {
    const flags = (output?.flags as string[]) ?? [];
    results.push({
      name: `flag:${flag}`,
      passed: flags.includes(flag),
      detail: flags.includes(flag) ? undefined : `missing flag ${flag}`,
    });
  }

  for (const artifact of goldenCase.expectedArtifacts ?? []) {
    const artifacts = (output?.artifacts as string[]) ?? [];
    results.push({
      name: `artifact:${artifact}`,
      passed: artifacts.includes(artifact),
      detail: artifacts.includes(artifact) ? undefined : `missing artifact ${artifact}`,
    });
  }

  return results;
}

// ---------- Scoring ----------

function combineScore(
  deterministic: DeterministicResult[],
  judge?: JudgeResult
): { overallScore: number; hardFailTriggered: boolean } {
  const deterministicFailed = deterministic.some((d) => !d.passed);
  const hardFailTriggered = judge?.hardFailTriggered ?? false;

  // Deterministic failures are treated as hard fails by default. Adjust if
  // some deterministic checks should only reduce the score instead.
  if (deterministicFailed || hardFailTriggered) {
    return { overallScore: judge?.overallScore ?? 0, hardFailTriggered: true };
  }
  return { overallScore: judge?.overallScore ?? 1, hardFailTriggered: false };
}

// ---------- Runner ----------

export async function runCase(goldenCase: GoldenCase): Promise<CaseResult> {
  const actualOutput = await runSystemUnderTest(goldenCase.input);
  const deterministic = runDeterministicChecks(goldenCase, actualOutput);

  const needsJudge = !!goldenCase.scoringWeights;
  const judge = needsJudge ? await callLlmJudge(goldenCase, actualOutput) : undefined;

  const { overallScore, hardFailTriggered } = combineScore(deterministic, judge);
  const passed = overallScore >= PASS_THRESHOLD && !hardFailTriggered;

  return {
    caseId: goldenCase.id,
    name: goldenCase.name,
    passed,
    overallScore,
    hardFailTriggered,
    deterministic,
    judge,
    notes: judge?.notes ?? "",
  };
}

export async function runSuite(cases: GoldenCase[]): Promise<RunReport> {
  const results: CaseResult[] = [];
  // Aggregate up, category down: the per-category breakdown is the regression
  // ratchet — no category should ship below its previous score.
  const byCategory: Record<string, CategoryStats> = {};
  for (const c of cases) {
    const result = await runCase(c);
    results.push(result);

    const category = c.labels?.category ?? "uncategorized";
    const stats = byCategory[category] ?? { total: 0, passed: 0 };
    stats.total += 1;
    if (result.passed) stats.passed += 1;
    byCategory[category] = stats;
  }

  const passed = results.filter((r) => r.passed).length;
  const hardFailures = results.filter((r) => r.hardFailTriggered).map((r) => r.caseId);
  const passRate = results.length ? passed / results.length : 0;

  const releaseRecommendation =
    hardFailures.length === 0 && passRate >= RELEASE_PASS_RATE ? "SHIP" : "BLOCK";

  return {
    total: results.length,
    passed,
    failed: results.length - passed,
    passRate,
    hardFailures,
    byCategory,
    results,
    releaseRecommendation,
  };
}

// ---------- Entry point ----------

async function main(): Promise<void> {
  const fs = await import("node:fs/promises");
  const paths = process.argv.slice(2);
  if (paths.length === 0) {
    console.error("Usage: ts-node eval-runner-template.ts <golden-case.json ...>");
    process.exit(2);
  }

  const cases: GoldenCase[] = [];
  for (const p of paths) {
    cases.push(JSON.parse(await fs.readFile(p, "utf8")) as GoldenCase);
  }

  const report = await runSuite(cases);
  await fs.writeFile("eval-report.json", JSON.stringify(report, null, 2));

  console.log(`Pass rate: ${(report.passRate * 100).toFixed(1)}%`);
  for (const [category, stats] of Object.entries(report.byCategory)) {
    console.log(`  ${category}: ${stats.passed}/${stats.total}`);
  }
  console.log(`Hard failures: ${report.hardFailures.join(", ") || "none"}`);
  console.log(`Release: ${report.releaseRecommendation}`);

  process.exit(report.releaseRecommendation === "SHIP" ? 0 : 1);
}

if (require.main === module) {
  main().catch((err) => {
    console.error(err);
    process.exit(1);
  });
}
