import re

from .store import Chunk, InMemoryDocumentStore


def retrieve(store: InMemoryDocumentStore, query: str, top_k: int = 5) -> list[tuple[Chunk, float]]:
    terms = set(re.findall(r"[a-zA-Z0-9]{2,}", query.lower()))
    scored: list[tuple[Chunk, float]] = []
    for chunk in store.all_chunks():
        words = set(re.findall(r"[a-zA-Z0-9]{2,}", chunk.text.lower()))
        overlap = len(terms & words)
        if overlap:
            scored.append((chunk, overlap / max(len(terms), 1)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:top_k]
