import os
import time
import uuid
from dataclasses import dataclass, field
from typing import Any

import httpx


@dataclass
class GatewayMetrics:
    requests: int = 0
    failures: int = 0
    fallback_requests: int = 0
    total_latency_ms: float = 0
    total_tokens: int = 0
    request_ids: list[str] = field(default_factory=list)

    def snapshot(self) -> dict[str, int | float]:
        average_latency = self.total_latency_ms / self.requests if self.requests else 0
        return {
            "requests": self.requests,
            "failures": self.failures,
            "fallback_requests": self.fallback_requests,
            "average_latency_ms": round(average_latency, 2),
            "total_tokens": self.total_tokens,
        }


class LLMGateway:
    def __init__(self) -> None:
        self.base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self.api_key = os.getenv("OPENAI_API_KEY", "")
        self.primary_model = os.getenv("GATEWAY_PRIMARY_MODEL", os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
        self.fallback_model = os.getenv("GATEWAY_FALLBACK_MODEL", self.primary_model)
        self.timeout = float(os.getenv("LLM_TIMEOUT_SECONDS", "60"))
        self.metrics = GatewayMetrics()

    def complete(self, payload: dict[str, Any]) -> tuple[dict[str, Any], str, str, float]:
        request_id = uuid.uuid4().hex
        started = time.perf_counter()
        self.metrics.requests += 1
        try:
            response, model = self._send(payload, self.primary_model)
        except httpx.HTTPError:
            self.metrics.failures += 1
            if self.fallback_model == self.primary_model:
                raise
            self.metrics.fallback_requests += 1
            response, model = self._send(payload, self.fallback_model)
        latency_ms = (time.perf_counter() - started) * 1000
        self.metrics.total_latency_ms += latency_ms
        self.metrics.total_tokens += int(response.get("usage", {}).get("total_tokens", 0))
        self.metrics.request_ids.append(request_id)
        return response, model, request_id, latency_ms

    def _send(self, payload: dict[str, Any], model: str) -> tuple[dict[str, Any], str]:
        body = {**payload, "model": model}
        response = httpx.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"},
            json=body,
            timeout=self.timeout,
        )
        response.raise_for_status()
        return response.json(), model

