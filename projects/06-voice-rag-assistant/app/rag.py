import json
from dataclasses import asdict, dataclass
from pathlib import Path

import numpy as np


@dataclass
class Chunk:
    chunk_id: str
    source: str
    text: str
    vector: list[float]


def split_text(text: str, size: int = 90, overlap: int = 18) -> list[str]:
    words = text.split()
    chunks = []
    step = max(size - overlap, 1)
    for start in range(0, len(words), step):
        chunk = " ".join(words[start : start + size]).strip()
        if chunk:
            chunks.append(chunk)
        if start + size >= len(words):
            break
    return chunks


class VoiceKnowledgeBase:
    def __init__(self, document_path: Path, index_path: Path, embedder) -> None:
        self.document_path = document_path
        self.index_path = index_path
        self.embedder = embedder
        self.chunks: list[Chunk] = []
        self.load()

    def load(self) -> None:
        if self.index_path.exists():
            items = json.loads(self.index_path.read_text(encoding="utf-8"))
            self.chunks = [Chunk(**item) for item in items]

    def ingest(self) -> int:
        texts = split_text(self.document_path.read_text(encoding="utf-8"))
        vectors = self.embedder.embed(texts)
        self.chunks = [
            Chunk(f"{self.document_path.stem}-{index + 1}", self.document_path.name, text, vector)
            for index, (text, vector) in enumerate(zip(texts, vectors))
        ]
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        self.index_path.write_text(json.dumps([asdict(chunk) for chunk in self.chunks]), encoding="utf-8")
        return len(self.chunks)

    def search(self, query: str, limit: int = 4) -> list[Chunk]:
        if not self.chunks:
            return []
        query_vector = np.array(self.embedder.embed([query])[0], dtype=float)
        query_norm = np.linalg.norm(query_vector)
        scored = []
        for chunk in self.chunks:
            vector = np.array(chunk.vector, dtype=float)
            denominator = query_norm * np.linalg.norm(vector)
            score = float(np.dot(query_vector, vector) / denominator) if denominator else 0.0
            scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:limit]]
