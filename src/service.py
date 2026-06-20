from pathlib import Path

from src.chatbot import UniversityChatbot
from src.retriever import FAQRetriever, RetrievedChunk

EXAMPLE_QUESTIONS = [
    "What are the admission requirements?",
    "How do I apply for financial aid?",
    "When is the scholarship application deadline?",
    "How do I register for classes?",
    "What student support services are available?",
]


def _find_faq_path() -> Path:
    base_dir = Path(__file__).resolve().parent.parent
    candidates = [
        base_dir / "data" / "faq.json",
        Path.cwd() / "data" / "faq.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "FAQ file not found. Expected data/faq.json in the project directory."
    )


class ChatService:
    def __init__(self) -> None:
        self.retriever = FAQRetriever(faq_path=_find_faq_path())
        self.chatbot = UniversityChatbot(retriever=self.retriever)
        self._loaded = False

    def ensure_loaded(self) -> None:
        if not self._loaded:
            print("Loading models and FAQ index...")
            self.chatbot.load()
            self._loaded = True

    def ask(self, message: str) -> dict:
        self.ensure_loaded()

        if not message.strip():
            return {
                "answer": "Please enter a university-related question.",
                "sources": [],
            }

        answer, chunks = self.chatbot.respond(message)
        return {
            "answer": answer,
            "sources": [self._format_source(chunk) for chunk in chunks],
        }

    @staticmethod
    def _format_source(chunk: RetrievedChunk) -> dict:
        return {
            "category": chunk.category,
            "question": chunk.question,
            "score": round(chunk.score, 2),
        }

    @staticmethod
    def get_examples() -> list[str]:
        return EXAMPLE_QUESTIONS


chat_service = ChatService()
