from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile

from .config import get_config
from .elevenlabs import ElevenLabsClient
from .llm import LLMClient
from .pipeline import VoiceRAGAssistant
from .rag import VoiceKnowledgeBase

ROOT = Path(__file__).resolve().parents[1]
config = get_config()
llm = LLMClient(config)
speech = ElevenLabsClient(config)
knowledge_base = VoiceKnowledgeBase(ROOT / "data" / "support-center-handbook.md", ROOT / "data" / "index.json", llm)
assistant = VoiceRAGAssistant(speech, llm, knowledge_base)
app = FastAPI(title="Voice RAG Assistant", version="1.0.0")


@app.get("/health")
def health() -> dict[str, int | str]:
    return {"status": "ok", "indexed_chunks": len(knowledge_base.chunks)}


@app.post("/ingest")
def ingest() -> dict[str, int | str]:
    try:
        count = knowledge_base.ingest()
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Knowledge base indexing failed: {error}") from error
    return {"status": "indexed", "chunks": count}


@app.post("/voice-query")
async def voice_query(audio: UploadFile = File(...), limit: int = 4) -> dict[str, object]:
    if not 1 <= limit <= 8:
        raise HTTPException(status_code=422, detail="limit must be between 1 and 8")
    if not knowledge_base.chunks:
        raise HTTPException(status_code=409, detail="Index is empty. Call /ingest first.")
    content = await audio.read()
    if not content:
        raise HTTPException(status_code=400, detail="Audio file is empty")
    content_type = audio.content_type or "application/octet-stream"
    try:
        result = assistant.answer(content, audio.filename or "voice-message", content_type, limit)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
    except Exception as error:
        raise HTTPException(status_code=502, detail=f"Voice pipeline failed: {error}") from error
    return {
        "transcript": result.transcript,
        "answer": result.answer,
        "audio_content_type": "audio/mpeg",
        "audio_base64": assistant.audio_base64(result.audio),
        "sources": [{"id": item.chunk_id, "source": item.source, "text": item.text} for item in result.sources],
    }
