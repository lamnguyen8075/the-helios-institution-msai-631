from transformers import pipeline

from src.retriever import FAQRetriever, RetrievedChunk


FALLBACK_MESSAGE = (
    "I could not find a confident answer in the Helios Institution FAQ. "
    "Please try rephrasing your question or contact the admissions "
    "or student services office directly."
)

SYSTEM_PROMPT = (
    "You are a helpful Helios Institution student support assistant. "
    "Answer using only the provided FAQ context. "
    "If the context does not contain the answer, say you do not know. "
    "Keep responses concise, friendly, and accurate."
)


class UniversityChatbot:
    def __init__(
        self,
        retriever: FAQRetriever,
        model_name: str = "google/flan-t5-base",
    ):
        self.retriever = retriever
        self.model_name = model_name
        self.generator = None

    def load(self) -> None:
        self.retriever.load()
        self.generator = pipeline(
            "text2text-generation",
            model=self.model_name,
        )

    def _build_prompt(self, user_message: str, chunks: list[RetrievedChunk]) -> str:
        context = FAQRetriever.format_context(chunks)
        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"FAQ Context:\n{context}\n\n"
            f"Student question: {user_message}\n"
            f"Helpful answer:"
        )

    def respond(self, user_message: str) -> tuple[str, list[RetrievedChunk]]:
        if not user_message.strip():
            return "Please enter a Helios Institution-related question.", []

        chunks = self.retriever.retrieve(user_message)

        if not chunks or chunks[0].score < self.retriever.score_threshold:
            return FALLBACK_MESSAGE, chunks

        prompt = self._build_prompt(user_message, chunks)
        result = self.generator(
            prompt,
            max_new_tokens=180,
            do_sample=False,
        )
        answer = result[0]["generated_text"].strip()
        return answer, chunks

    @staticmethod
    def format_sources(chunks: list[RetrievedChunk]) -> str:
        if not chunks:
            return ""

        lines = ["**Sources:**"]
        for chunk in chunks:
            lines.append(
                f"- {chunk.category}: {chunk.question} (score: {chunk.score:.2f})"
            )
        return "\n".join(lines)
