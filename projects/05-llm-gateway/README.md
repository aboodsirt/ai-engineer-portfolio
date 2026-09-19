# LLM Gateway

An OpenAI-compatible gateway that gives application teams one stable endpoint while handling provider details behind it.

It adds request IDs, latency and usage tracking, retryable failure handling, and a fallback model. The upstream contract stays compatible with `/v1/chat/completions`, which makes it easy to place in front of existing applications.

## Run

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8010
```

Point an OpenAI-compatible client at `http://127.0.0.1:8010/v1` and use any key accepted by the configured upstream.

