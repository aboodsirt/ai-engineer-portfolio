# AI Engineer Portfolio Lab

Six focused AI engineering projects built around retrieval augmented generation, tool calling, agent orchestration, evaluation, reliable LLM infrastructure, and voice interfaces.

## Projects

| Project | What it demonstrates | Run it |
| --- | --- | --- |
| [01 RAG Knowledge Base](projects/01-rag-knowledge-base) | Chunking, embeddings, cosine retrieval, grounded answers, citations | `uvicorn app.main:app --reload` |
| [02 Tool Calling Agent](projects/02-tool-calling-agent) | Typed tools, multi-step tool loops, safe calculator and knowledge search | `uvicorn app.main:app --reload` |
| [03 Research Brief Agent](projects/03-research-brief-agent) | Planner, parallel source workers, synthesis, source-aware output | `uvicorn app.main:app --reload` |
| [04 LLM Evaluation Harness](projects/04-llm-evaluation-harness) | Dataset-driven scoring, judge prompts, aggregate quality metrics | `python -m app.evaluate` |
| [05 LLM Gateway](projects/05-llm-gateway) | Timeouts, retries, fallback models, usage tracking, request IDs | `uvicorn app.main:app --reload` |
| [06 Voice RAG Assistant](projects/06-voice-rag-assistant) | ElevenLabs speech-to-text, RAG grounding, OpenAI-compatible chat, ElevenLabs voice synthesis | `uvicorn app.main:app --reload` |

Each project has its own README, dependency file, tests where useful, and a small sample dataset. The projects share an OpenAI-compatible API contract, so keys and model choices live in environment variables rather than source code.

## Quick start

```powershell
Copy-Item .env.example .env
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r projects\01-rag-knowledge-base\requirements.txt
```

Run a project from its directory so its `app` package is on the Python path.

## Resume-ready impact statements

- Built a production-style RAG service with persistent vector indexing, semantic retrieval, grounded prompts, and source citations.
- Developed a tool-calling agent with typed function schemas, controlled execution, and iterative planning over multiple tool calls.
- Orchestrated a research workflow that separates planning, source collection, and synthesis while preserving traceable references.
- Created an LLM evaluation harness that scores answer relevance, groundedness, and context coverage over a repeatable dataset.
- Implemented an OpenAI-compatible LLM gateway with timeouts, retries, model fallback, request tracing, and usage accounting.
- Built a voice-first RAG assistant that transcribes user audio, retrieves grounded support context, and returns an ElevenLabs-generated voice answer.

## Engineering choices

The code stays intentionally small and readable while showing the boundaries that matter in real AI systems: provider clients, domain logic, persistence, HTTP APIs, validation, and tests. No API keys are committed.
