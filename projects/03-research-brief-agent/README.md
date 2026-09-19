# Research Brief Agent

A multi-agent workflow for producing a source-aware research brief from a question and a list of public URLs.

The planner creates focused research questions, source workers fetch and clean each page concurrently, and the synthesizer turns the collected evidence into a brief with inline source labels.

## Run

```powershell
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Request body:

```json
{
  "question": "What are the main design tradeoffs in retrieval augmented generation?",
  "sources": ["https://example.com/article"]
}
```

