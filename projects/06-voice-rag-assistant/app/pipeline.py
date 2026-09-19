import base64
from dataclasses import dataclass

from .rag import Chunk, VoiceKnowledgeBase


@dataclass
class VoiceResult:
    transcript: str
    answer: str
    audio: bytes
    sources: list[Chunk]


class VoiceRAGAssistant:
    def __init__(self, speech, llm, knowledge_base: VoiceKnowledgeBase) -> None:
        self.speech = speech
        self.llm = llm
        self.knowledge_base = knowledge_base

    def answer(self, audio: bytes, filename: str, content_type: str, limit: int = 4) -> VoiceResult:
        transcript = self.speech.transcribe(audio, filename, content_type)
        matches = self.knowledge_base.search(transcript, limit)
        if not matches:
            raise ValueError("The knowledge base is empty. Call /ingest first.")
        context = "\n\n".join(f"[{item.chunk_id}] {item.text}" for item in matches)
        answer = self.llm.chat(
            "You are a voice support assistant. Answer only from the supplied context. If the context is insufficient, say that you do not know. Keep the answer concise and mention source IDs in square brackets.",
            f"Context:\n{context}\n\nVoice transcript: {transcript}",
        )
        return VoiceResult(transcript, answer, self.speech.synthesize(answer), matches)

    @staticmethod
    def audio_base64(audio: bytes) -> str:
        return base64.b64encode(audio).decode("ascii")
