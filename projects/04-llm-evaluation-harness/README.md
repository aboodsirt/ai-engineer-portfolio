# LLM Evaluation Harness

A repeatable evaluation runner for RAG or agent responses. It loads JSONL cases, sends a structured judge prompt to an LLM, validates the result, and writes aggregate metrics for answer relevance, groundedness, and context coverage.

## Run

```powershell
pip install -r requirements.txt
python -m app.evaluate --dataset data\examples.jsonl
```

The output contains per-case scores, the failed criteria, and a summary that can be stored in CI artifacts or compared between prompt versions.

