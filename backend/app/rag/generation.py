from .store import Chunk


def compose_answer(question: str, matches: list[tuple[Chunk, float]]) -> str:
    if not matches:
        return "I couldn't find that in the uploaded documents. Try rephrasing the question or upload a relevant source."
    excerpts = " ".join(chunk.text for chunk, _ in matches[:2])
    return f"Based on the uploaded documents: {excerpts}"
