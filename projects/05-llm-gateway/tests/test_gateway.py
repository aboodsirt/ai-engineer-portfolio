from app.gateway import GatewayMetrics


def test_metrics_snapshot_handles_empty_state():
    assert GatewayMetrics().snapshot() == {"requests": 0, "failures": 0, "fallback_requests": 0, "average_latency_ms": 0, "total_tokens": 0}


def test_metrics_snapshot_calculates_average_latency():
    metrics = GatewayMetrics(requests=2, total_latency_ms=80, total_tokens=24)
    assert metrics.snapshot()["average_latency_ms"] == 40.0

