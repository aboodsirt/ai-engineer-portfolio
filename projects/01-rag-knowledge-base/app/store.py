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


def split_text(text: str, size: int = 700, overlap: int = 100) -> list[str]:
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


class VectorStore:
    def __init__(self, path: Path) -> None:
        self.path = path
        self.chunks: list[Chunk] = []
        self.load()

    def load(self) -> None:
        if not self.path.exists():
            return
        items = json.loads(self.path.read_text(encoding="utf-8"))
        self.chunks = [Chunk(**item) for item in items]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text(json.dumps([asdict(chunk) for chunk in self.chunks]), encoding="utf-8")

    def replace(self, chunks: list[Chunk]) -> None:
        self.chunks = chunks
        self.save()

    def search(self, query: list[float], limit: int = 4) -> list[Chunk]:
        if not self.chunks:
            return []
        query_vector = np.array(query, dtype=float)
        query_norm = np.linalg.norm(query_vector)
        scored = []
        for chunk in self.chunks:
            vector = np.array(chunk.vector, dtype=float)
            denominator = query_norm * np.linalg.norm(vector)
            score = float(np.dot(query_vector, vector) / denominator) if denominator else 0.0
            scored.append((score, chunk))
        scored.sort(key=lambda item: item[0], reverse=True)
        return [chunk for _, chunk in scored[:limit]]

