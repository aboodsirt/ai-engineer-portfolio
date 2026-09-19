# RAG Knowledge Base

A small FastAPI service that turns Markdown notes into an embedding index and answers questions with retrieved context and citations.

## Flow

1. Markdown files are split into overlapping chunks.
2. The embedding endpoint creates a vector for each chunk.
3. Cosine similarity ranks the most relevant chunks.
4. The chat model receives only the selected context and must cite source IDs.

## Run

```powershell
pip install -r requirements.txt
Copy-Item ..\..\.env.example .env
uvicorn app.main:app --reload
```

In another terminal:

```powershell
Invoke-RestMethod -Method Post http://127.0.0.1:8000/ingest
Invoke-RestMethod -Method Post http://127.0.0.1:8000/ask -ContentType 'application/json' -Body '{"question":"How does the support escalation policy work?"}'
```

