import json
import os
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import httpx
from pydantic import BaseModel, Field, ValidationError


class EvaluationCase(BaseModel):
    id: str
    question: str
    context: str
    answer: str
    reference: str


class JudgeResult(BaseModel):
    relevance: int = Field(ge=1, le=5)
    groundedness: int = Field(ge=1, le=5)
    context_coverage: int = Field(ge=1, le=5)
    rationale: str


@dataclass
class CaseScore:
    case_id: str
    relevance: int
    groundedness: int
    context_coverage: int
    rationale: str


def average(values: list[int]) -> float:
    return round(sum(values) / len(values), 2) if values else 0.0


def summarize(scores: list[CaseScore]) -> dict[str, Any]:
    return {
        "cases": len(scores),
        "relevance": average([score.relevance for score in scores]),
        "groundedness": average([score.groundedness for score in scores]),
        "context_coverage": average([score.context_coverage for score in scores]),
        "overall": average([score.relevance + score.groundedness + score.context_coverage for score in scores]) / 3,
    }


class LLMJudge:
    def __init__(self) -> None:
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        self.timeout = float(os.getenv("LLM_TIMEOUT_SECONDS", "60"))

    def score(self, case: EvaluationCase) -> JudgeResult:
        prompt = json.dumps(case.model_dump())
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json={
                "model": self.model,
                "temperature": 0,
                "response_format": {"type": "json_object"},
                "messages": [
                    {"role": "system", "content": "You are an LLM evaluation judge. Score relevance, groundedness, and context coverage from 1 to 5. Return only JSON with integer scores and a short rationale."},
                    {"role": "user", "content": prompt},
                ],
            },
            timeout=self.timeout,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        try:
            return JudgeResult.model_validate_json(content)
        except ValidationError as error:
            raise ValueError(f"Judge returned invalid JSON: {error}") from error


def load_cases(path: Path) -> list[EvaluationCase]:
    return [EvaluationCase.model_validate_json(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def evaluate(path: Path, judge: LLMJudge | None = None) -> dict[str, Any]:
    active_judge = judge or LLMJudge()
    scores = []
    for case in load_cases(path):
        result = active_judge.score(case)
        scores.append(CaseScore(case.id, result.relevance, result.groundedness, result.context_coverage, result.rationale))
    return {"summary": summarize(scores), "scores": [asdict(score) for score in scores]}

