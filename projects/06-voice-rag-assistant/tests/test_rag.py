from pathlib import Path

from app.rag import VoiceKnowledgeBase, split_text


class FakeEmbedder:
    def embed(self, texts):
        return [[float(len(text)), 1.0] for text in texts]


def test_split_text_preserves_short_document():
    assert split_text("one two three", size=10) == ["one two three"]


def test_ingest_and_search(tmp_path: Path):
    document = tmp_path / "handbook.md"
    document.write_text("refund policy details", encoding="utf-8")
    store = VoiceKnowledgeBase(document, tmp_path / "index.json", FakeEmbedder())
    assert store.ingest() == 1
    assert store.search("refund", 1)[0].source == "handbook.md"
