"""Starter eval runner. Replace the placeholder functions
(`run_system_under_test`, `call_llm_judge`) with real implementations.

Usage:
    python eval-runner-template.py ./golden/*.json
    (or wire into your existing test command / CI job)

Requires Python 3.10+. Reads the same camelCase golden-case JSON as the
TypeScript runner and writes an eval-report.json with the same shape.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from typing import Any, Literal

# ---------- Types ----------


@dataclass
class HardFailGate:
    id: str
    description: str


@dataclass
class GoldenCase:
    id: str
    name: str
    prd_requirement_ids: list[str]
    scenario: str
    input: Any
    expected_output: Any
    user_persona: str | None = None
    expected_flags: list[str] = field(default_factory=list)
    expected_artifacts: list[str] = field(default_factory=list)
    hard_fail_gates: list[HardFailGate] = field(default_factory=list)
    scoring_weights: dict[str, float] | None = None
    labels: dict[str, str] | None = None
    source: str | None = None
    human_score: float | None = None
    notes: str = ""

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> "GoldenCase":
        """Load a golden case from the camelCase JSON schema."""
        return cls(
            id=data["id"],
            name=data["name"],
            prd_requirement_ids=data["prdRequirementIds"],
            scenario=data["scenario"],
            input=data["input"],
            expected_output=data["expectedOutput"],
            user_persona=data.get("userPersona"),
            expected_flags=data.get("expectedFlags", []),
            expected_artifacts=data.get("expectedArtifacts", []),
            hard_fail_gates=[
                HardFailGate(id=g["id"], description=g["description"])
                for g in data.get("hardFailGates", [])
            ],
            scoring_weights=data.get("scoringWeights"),
            labels=data.get("labels"),
            source=data.get("source"),
            human_score=data.get("humanScore"),
            notes=data.get("notes", ""),
        )


@dataclass
class DeterministicResult:
    name: str
    passed: bool
    detail: str | None = None

    def to_json(self) -> dict[str, Any]:
        return {"name": self.name, "passed": self.passed, "detail": self.detail}


@dataclass
class JudgeResult:
    passed: bool
    overall_score: float
    scores: dict[str, float]
    hard_fail_triggered: bool
    missing_requirements: list[str]
    incorrect_claims: list[str]
    notes: str

    def to_json(self) -> dict[str, Any]:
        return {
            "passed": self.passed,
            "overallScore": self.overall_score,
            "scores": self.scores,
            "hardFailTriggered": self.hard_fail_triggered,
            "missingRequirements": self.missing_requirements,
            "incorrectClaims": self.incorrect_claims,
            "notes": self.notes,
        }


@dataclass
class CaseResult:
    case_id: str
    name: str
    passed: bool
    overall_score: float
    hard_fail_triggered: bool
    deterministic: list[DeterministicResult]
    judge: JudgeResult | None
    notes: str

    def to_json(self) -> dict[str, Any]:
        return {
            "caseId": self.case_id,
            "name": self.name,
            "passed": self.passed,
            "overallScore": self.overall_score,
            "hardFailTriggered": self.hard_fail_triggered,
            "deterministic": [d.to_json() for d in self.deterministic],
            "judge": self.judge.to_json() if self.judge else None,
            "notes": self.notes,
        }


@dataclass
class CategoryStats:
    total: int = 0
    passed: int = 0

    def to_json(self) -> dict[str, Any]:
        return {"total": self.total, "passed": self.passed}


@dataclass
class RunReport:
    total: int
    passed: int
    failed: int
    pass_rate: float
    hard_failures: list[str]
    by_category: dict[str, CategoryStats]
    results: list[CaseResult]
    release_recommendation: Literal["SHIP", "BLOCK"]

    def to_json(self) -> dict[str, Any]:
        return {
            "total": self.total,
            "passed": self.passed,
            "failed": self.failed,
            "passRate": self.pass_rate,
            "hardFailures": self.hard_failures,
            "byCategory": {k: v.to_json() for k, v in self.by_category.items()},
            "results": [r.to_json() for r in self.results],
            "releaseRecommendation": self.release_recommendation,
        }


# ---------- Config ----------

PASS_THRESHOLD: float = 0.85  # TODO: set from PRD quality bar
RELEASE_PASS_RATE: float = 0.9  # TODO: set from CI/release gate policy

# ---------- Placeholders (implement these) ----------


def run_system_under_test(input: Any) -> Any:
    """Run the product/system under test against a case's input."""
    # TODO: call the real system.
    raise NotImplementedError("run_system_under_test not implemented")


def call_llm_judge(golden_case: GoldenCase, actual_output: Any) -> JudgeResult:
    """Call the LLM judge for subjective dimensions. Return parsed JSON."""
    # TODO: render the judge prompt template, call the model, parse the JSON.
    raise NotImplementedError("call_llm_judge not implemented")


# ---------- Deterministic checks ----------


def run_deterministic_checks(
    golden_case: GoldenCase, actual_output: Any
) -> list[DeterministicResult]:
    """Assertions that need no LLM. Extend per product:
    presence of expected flags, artifacts, exact fields, counts, links, etc.
    """
    results: list[DeterministicResult] = []
    output: dict[str, Any] = actual_output if isinstance(actual_output, dict) else {}

    for flag in golden_case.expected_flags:
        flags: list[str] = output.get("flags") or []
        results.append(
            DeterministicResult(
                name=f"flag:{flag}",
                passed=flag in flags,
                detail=None if flag in flags else f"missing flag {flag}",
            )
        )

    for artifact in golden_case.expected_artifacts:
        artifacts: list[str] = output.get("artifacts") or []
        results.append(
            DeterministicResult(
                name=f"artifact:{artifact}",
                passed=artifact in artifacts,
                detail=None if artifact in artifacts else f"missing artifact {artifact}",
            )
        )

    return results


# ---------- Scoring ----------


def combine_score(
    deterministic: list[DeterministicResult], judge: JudgeResult | None
) -> tuple[float, bool]:
    """Return (overall_score, hard_fail_triggered)."""
    deterministic_failed = any(not d.passed for d in deterministic)
    hard_fail_triggered = judge.hard_fail_triggered if judge else False

    # Deterministic failures are treated as hard fails by default. Adjust if
    # some deterministic checks should only reduce the score instead.
    if deterministic_failed or hard_fail_triggered:
        return (judge.overall_score if judge else 0.0, True)
    return (judge.overall_score if judge else 1.0, False)


# ---------- Runner ----------


def run_case(golden_case: GoldenCase) -> CaseResult:
    actual_output = run_system_under_test(golden_case.input)
    deterministic = run_deterministic_checks(golden_case, actual_output)

    needs_judge = bool(golden_case.scoring_weights)
    judge = call_llm_judge(golden_case, actual_output) if needs_judge else None

    overall_score, hard_fail_triggered = combine_score(deterministic, judge)
    passed = overall_score >= PASS_THRESHOLD and not hard_fail_triggered

    return CaseResult(
        case_id=golden_case.id,
        name=golden_case.name,
        passed=passed,
        overall_score=overall_score,
        hard_fail_triggered=hard_fail_triggered,
        deterministic=deterministic,
        judge=judge,
        notes=judge.notes if judge else "",
    )


def run_suite(cases: list[GoldenCase]) -> RunReport:
    results: list[CaseResult] = []
    # Aggregate up, category down: the per-category breakdown is the regression
    # ratchet — no category should ship below its previous score.
    by_category: dict[str, CategoryStats] = {}
    for c in cases:
        result = run_case(c)
        results.append(result)

        category = (c.labels or {}).get("category", "uncategorized")
        stats = by_category.setdefault(category, CategoryStats())
        stats.total += 1
        if result.passed:
            stats.passed += 1

    passed = sum(1 for r in results if r.passed)
    hard_failures = [r.case_id for r in results if r.hard_fail_triggered]
    pass_rate = passed / len(results) if results else 0.0

    release_recommendation: Literal["SHIP", "BLOCK"] = (
        "SHIP" if not hard_failures and pass_rate >= RELEASE_PASS_RATE else "BLOCK"
    )

    return RunReport(
        total=len(results),
        passed=passed,
        failed=len(results) - passed,
        pass_rate=pass_rate,
        hard_failures=hard_failures,
        by_category=by_category,
        results=results,
        release_recommendation=release_recommendation,
    )


# ---------- Entry point ----------


def main() -> None:
    paths = sys.argv[1:]
    if not paths:
        print("Usage: python eval-runner-template.py <golden-case.json ...>", file=sys.stderr)
        sys.exit(2)

    cases: list[GoldenCase] = []
    for p in paths:
        with open(p, encoding="utf-8") as f:
            cases.append(GoldenCase.from_json(json.load(f)))

    report = run_suite(cases)
    with open("eval-report.json", "w", encoding="utf-8") as f:
        json.dump(report.to_json(), f, indent=2)

    print(f"Pass rate: {report.pass_rate * 100:.1f}%")
    for category, stats in report.by_category.items():
        print(f"  {category}: {stats.passed}/{stats.total}")
    print(f"Hard failures: {', '.join(report.hard_failures) or 'none'}")
    print(f"Release: {report.release_recommendation}")

    sys.exit(0 if report.release_recommendation == "SHIP" else 1)


if __name__ == "__main__":
    main()
