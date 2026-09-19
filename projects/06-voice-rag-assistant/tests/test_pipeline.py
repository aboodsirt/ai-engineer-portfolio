from app.pipeline import VoiceRAGAssistant
from app.rag import Chunk


class FakeSpeech:
    def transcribe(self, audio, filename, content_type):
        return "How long do refunds take?"

    def synthesize(self, text):
        return b"mp3-audio"


class FakeLLM:
    def chat(self, system, user):
        assert "refund" in user.lower()
        return "Approved refunds arrive within five to ten business days. [handbook-1]"


class FakeKnowledgeBase:
    def search(self, query, limit):
        return [Chunk("handbook-1", "handbook.md", "Refunds arrive within five to ten business days.", [1.0])]


def test_voice_rag_pipeline_returns_grounded_audio():
    assistant = VoiceRAGAssistant(FakeSpeech(), FakeLLM(), FakeKnowledgeBase())
    result = assistant.answer(b"input", "question.wav", "audio/wav")
    assert result.transcript.startswith("How long")
    assert result.answer.startswith("Approved refunds")
    assert result.audio == b"mp3-audio"
    assert assistant.audio_base64(result.audio) == "bXAzLWF1ZGlv"
