import json
from dataclasses import dataclass
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


@dataclass
class RetrievedChunk:
    question: str
    answer: str
    category: str
    score: float


class FAQRetriever:
    def __init__(
        self,
        faq_path: str | Path,
        model_name: str = "sentence-transformers/all-MiniLM-L6-v2",
        top_k: int = 3,
        score_threshold: float = 0.35,
    ):
        self.faq_path = Path(faq_path)
        self.model_name = model_name
        self.top_k = top_k
        self.score_threshold = score_threshold

        self.entries: list[dict] = []
        self.index: faiss.IndexFlatIP | None = None
        self.embedder: SentenceTransformer | None = None

    def load(self) -> None:
        with self.faq_path.open(encoding="utf-8") as file:
            self.entries = json.load(file)

        texts = [
            f"{entry['category']}: {entry['question']} {entry['answer']}"
            for entry in self.entries
        ]

        self.embedder = SentenceTransformer(self.model_name)
        embeddings = self.embedder.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype("float32")

        self.index = faiss.IndexFlatIP(embeddings.shape[1])
        self.index.add(embeddings)

    def retrieve(self, query: str) -> list[RetrievedChunk]:
        if self.index is None or self.embedder is None:
            raise RuntimeError("Retriever not loaded. Call load() first.")

        query_embedding = self.embedder.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
        ).astype("float32")

        scores, indices = self.index.search(query_embedding, self.top_k)
        results: list[RetrievedChunk] = []

        for score, index in zip(scores[0], indices[0]):
            if index < 0:
                continue

            entry = self.entries[index]
            results.append(
                RetrievedChunk(
                    question=entry["question"],
                    answer=entry["answer"],
                    category=entry["category"],
                    score=float(score),
                )
            )

        return results

    def has_relevant_context(self, query: str) -> bool:
        results = self.retrieve(query)
        return bool(results) and results[0].score >= self.score_threshold

    @staticmethod
    def format_context(chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return "No relevant university information was found."

        lines = []
        for chunk in chunks:
            lines.append(
                f"Category: {chunk.category}\n"
                f"Question: {chunk.question}\n"
                f"Answer: {chunk.answer}"
            )
        return "\n\n".join(lines)
