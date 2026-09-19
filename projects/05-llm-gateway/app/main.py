from typing import Any

from fastapi import FastAPI, Header, HTTPException

from .gateway import LLMGateway

app = FastAPI(title="LLM Gateway", version="1.0.0")
gateway = LLMGateway()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/metrics")
def metrics() -> dict[str, int | float]:
    return gateway.metrics.snapshot()


@app.post("/v1/chat/completions")
def completions(payload: dict[str, Any], x_request_id: str | None = Header(default=None)) -> dict[str, Any]:
    if not payload.get("messages"):
        raise HTTPException(status_code=422, detail="messages is required")
    try:
        result, model, request_id, latency_ms = gateway.complete(payload)
    except Exception as error:
        raise HTTPException(status_code=502, detail=str(error)) from error
    result["model"] = model
    result["gateway"] = {"request_id": request_id, "upstream_request_id": x_request_id, "latency_ms": round(latency_ms, 2)}
    return result

