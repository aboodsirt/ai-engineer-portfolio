from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .config import get_config
from .llm import LLMClient
from .store import Chunk, VectorStore, split_text

ROOT = Path(__file__).resolve().parents[1]
config = get_config()
client = LLMClient(config)
store = VectorStore(ROOT / "data" / "index.json")
app = FastAPI(title="RAG Knowledge Base", version="1.0.0")


class Question(BaseModel):
    question: str = Field(min_length=3)
    limit: int = Field(default=4, ge=1, le=8)


@app.get("/health")
def health() -> dict[str, int | str]:
    return {"status": "ok", "chunks": len(store.chunks)}


@app.post("/ingest")
def ingest() -> dict[str, int | str]:
    documents = list((ROOT / "data").glob("*.md"))
    raw_chunks = []
    for document in documents:
        for index, text in enumerate(split_text(document.read_text(encoding="utf-8"))):
            raw_chunks.append((f"{document.stem}-{index + 1}", document.name, text))
    if not raw_chunks:
        raise HTTPException(status_code=400, detail="No Markdown documents found")
    vectors = client.embed([item[2] for item in raw_chunks])
    store.replace([Chunk(chunk_id=item[0], source=item[1], text=item[2], vector=vector) for item, vector in zip(raw_chunks, vectors)])
    return {"status": "indexed", "chunks": len(store.chunks)}


@app.post("/ask")
def ask(payload: Question) -> dict[str, object]:
    if not store.chunks:
        raise HTTPException(status_code=409, detail="Index is empty. Call /ingest first.")
    query_vector = client.embed([payload.question])[0]
    matches = store.search(query_vector, payload.limit)
    context = "\n\n".join(f"[{item.chunk_id}] {item.text}" for item in matches)
    answer = client.chat(
        "You answer questions only from the supplied context. If the context is insufficient, say so. Cite the chunk IDs used in square brackets.",
        f"Context:\n{context}\n\nQuestion: {payload.question}",
    )
    return {"answer": answer, "sources": [{"id": item.chunk_id, "source": item.source} for item in matches]}

