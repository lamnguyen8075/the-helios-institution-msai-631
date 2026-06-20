from pathlib import Path

import gradio as gr

from src.chatbot import UniversityChatbot
from src.retriever import FAQRetriever
from src.ui import (
    CUSTOM_CSS,
    EXAMPLE_QUESTIONS,
    FOOTER_HTML,
    HERO_HTML,
    SIDEBAR_HTML,
    build_theme,
)

BASE_DIR = Path(__file__).resolve().parent


def _find_faq_path() -> Path:
    candidates = [
        BASE_DIR / "data" / "faq.json",
        Path.cwd() / "data" / "faq.json",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    raise FileNotFoundError(
        "FAQ file not found. Expected data/faq.json in the project directory."
    )


FAQ_PATH = _find_faq_path()

retriever = FAQRetriever(faq_path=FAQ_PATH)
chatbot = UniversityChatbot(retriever=retriever)
_loaded = False


def ensure_loaded() -> None:
    global _loaded
    if not _loaded:
        print("Loading models and FAQ index...")
        chatbot.load()
        _loaded = True


def _format_answer(message: str) -> str:
    answer, chunks = chatbot.respond(message)
    sources = chatbot.format_sources(chunks)
    if sources:
        return f"{answer}\n\n{sources}"
    return answer


def chat(message: str, history: list | None) -> tuple[str, list]:
    ensure_loaded()
    history = history or []

    if not message.strip():
        return "", history

    bot_reply = _format_answer(message)
    return "", history + [[message, bot_reply]]


def fill_prompt(example: str) -> str:
    return example


def clear_chat() -> tuple[list, str]:
    return [], ""


def build_interface() -> gr.Blocks:
    theme = build_theme()
    quick_buttons: list[gr.Button] = []

    with gr.Blocks(
        title="Helios Institution Student Support Chatbot",
        theme=theme,
        css=CUSTOM_CSS,
    ) as demo:
        gr.HTML(HERO_HTML)

        with gr.Row(equal_height=False):
            with gr.Column(scale=1, min_width=280):
                gr.HTML(SIDEBAR_HTML)

                gr.Markdown("### Try asking")
                for question in EXAMPLE_QUESTIONS:
                    quick_buttons.append(
                        gr.Button(question, elem_classes=["quick-btn"])
                    )

            with gr.Column(scale=2, elem_classes=["chat-shell"]):
                chatbot_ui = gr.Chatbot(
                    label="Student Support Assistant",
                    height=460,
                    show_copy_button=True,
                    bubble_full_width=False,
                )

                user_input = gr.Textbox(
                    label="Your question",
                    placeholder="Ask about admissions, aid, enrollment, or student services...",
                    lines=2,
                    elem_classes=["chat-input"],
                )

                with gr.Row():
                    send_btn = gr.Button(
                        "Send",
                        variant="primary",
                        elem_classes=["send-btn"],
                    )
                    clear_btn = gr.Button(
                        "Clear conversation",
                        elem_classes=["clear-btn"],
                    )

        gr.HTML(FOOTER_HTML)

        send_btn.click(chat, [user_input, chatbot_ui], [user_input, chatbot_ui])
        user_input.submit(chat, [user_input, chatbot_ui], [user_input, chatbot_ui])
        clear_btn.click(clear_chat, None, [chatbot_ui, user_input])

        for button in quick_buttons:
            button.click(fill_prompt, None, user_input)

    return demo


def main() -> None:
    ensure_loaded()
    print("Starting Gradio app...")
    build_interface().launch(
        server_name="127.0.0.1",
        server_port=7860,
        show_error=True,
    )


if __name__ == "__main__":
    main()
