import gradio as gr

# University-inspired palette: deep navy, warm gold, soft parchment
COLORS = {
    "navy": "#1a2f4a",
    "navy_light": "#2d4a6f",
    "gold": "#c9a227",
    "gold_soft": "#e8d5a3",
    "cream": "#faf8f3",
    "mist": "#eef2f7",
    "ink": "#1c2430",
    "slate": "#5c6b7a",
}

CUSTOM_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,700;1,500&family=Outfit:wght@300;400;500;600&display=swap');

:root {
    --navy: #1a2f4a;
    --gold: #c9a227;
    --cream: #faf8f3;
}

.gradio-container {
    max-width: 1180px !important;
    margin: 0 auto !important;
    font-family: 'Outfit', sans-serif !important;
    background: linear-gradient(165deg, #f7f9fc 0%, #eef2f7 45%, #e8edf4 100%) !important;
}

/* Hero */
.hero-shell {
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    padding: 2.4rem 2.6rem 2rem;
    margin-bottom: 1.4rem;
    background:
        radial-gradient(circle at 85% 15%, rgba(201, 162, 39, 0.22), transparent 42%),
        radial-gradient(circle at 10% 80%, rgba(45, 74, 111, 0.35), transparent 50%),
        linear-gradient(135deg, #1a2f4a 0%, #243f61 55%, #1a2f4a 100%);
    box-shadow: 0 24px 48px rgba(26, 47, 74, 0.18);
}

.hero-shell::before {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(255,255,255,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,0.04) 1px, transparent 1px);
    background-size: 28px 28px;
    opacity: 0.35;
    pointer-events: none;
}

.hero-kicker {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    padding: 0.35rem 0.85rem;
    border-radius: 999px;
    background: rgba(201, 162, 39, 0.16);
    border: 1px solid rgba(201, 162, 39, 0.35);
    color: #f3e4b8;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 0.9rem;
}

.hero-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: clamp(2.2rem, 4vw, 3.2rem) !important;
    font-weight: 700 !important;
    color: #ffffff !important;
    line-height: 1.08 !important;
    margin: 0 0 0.65rem 0 !important;
    letter-spacing: -0.02em;
}

.hero-subtitle {
    color: rgba(255, 255, 255, 0.82) !important;
    font-size: 1.02rem !important;
    line-height: 1.6 !important;
    max-width: 640px;
    margin: 0 !important;
}

.hero-badge-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem;
    margin-top: 1.2rem;
}

.hero-badge {
    padding: 0.35rem 0.75rem;
    border-radius: 999px;
    background: rgba(255, 255, 255, 0.08);
    border: 1px solid rgba(255, 255, 255, 0.14);
    color: rgba(255, 255, 255, 0.88);
    font-size: 0.8rem;
}

/* Layout cards */
.panel-card {
    background: rgba(255, 255, 255, 0.82);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(26, 47, 74, 0.08);
    border-radius: 20px;
    padding: 1.25rem;
    box-shadow: 0 12px 30px rgba(26, 47, 74, 0.06);
}

.panel-title {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.45rem !important;
    font-weight: 700 !important;
    color: var(--navy) !important;
    margin: 0 0 0.35rem 0 !important;
}

.panel-copy {
    color: #5c6b7a !important;
    font-size: 0.92rem !important;
    line-height: 1.55 !important;
    margin: 0 0 1rem 0 !important;
}

.topic-list {
    display: grid;
    gap: 0.55rem;
}

.topic-item {
    display: flex;
    align-items: center;
    gap: 0.65rem;
    padding: 0.7rem 0.85rem;
    border-radius: 14px;
    background: linear-gradient(135deg, #f8fafc, #f1f5f9);
    border: 1px solid rgba(26, 47, 74, 0.06);
}

.topic-dot {
    width: 9px;
    height: 9px;
    border-radius: 50%;
    background: var(--gold);
    flex-shrink: 0;
    box-shadow: 0 0 0 4px rgba(201, 162, 39, 0.15);
}

.topic-label {
    color: var(--navy);
    font-size: 0.88rem;
    font-weight: 500;
}

/* Quick prompts */
.quick-prompts label {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.15rem !important;
    font-weight: 700 !important;
    color: var(--navy) !important;
}

.quick-btn button {
    width: 100% !important;
    justify-content: flex-start !important;
    text-align: left !important;
    border-radius: 14px !important;
    border: 1px solid rgba(26, 47, 74, 0.1) !important;
    background: linear-gradient(180deg, #ffffff, #f7f9fc) !important;
    color: var(--navy) !important;
    font-weight: 500 !important;
    padding: 0.8rem 1rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(26, 47, 74, 0.04) !important;
}

.quick-btn button:hover {
    transform: translateY(-1px);
    border-color: rgba(201, 162, 39, 0.45) !important;
    box-shadow: 0 8px 20px rgba(26, 47, 74, 0.08) !important;
}

/* Chat area */
.chat-shell .label-wrap span {
    font-family: 'Cormorant Garamond', serif !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    color: var(--navy) !important;
}

.chat-shell .chatbot {
    border-radius: 18px !important;
    border: 1px solid rgba(26, 47, 74, 0.08) !important;
    background: linear-gradient(180deg, #ffffff 0%, #fbfcfe 100%) !important;
    min-height: 420px !important;
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.8);
}

.chat-shell .message.user {
    background: linear-gradient(135deg, #1a2f4a, #2d4a6f) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 18px 18px 4px 18px !important;
}

.chat-shell .message.bot {
    background: #ffffff !important;
    color: #1c2430 !important;
    border: 1px solid rgba(26, 47, 74, 0.08) !important;
    border-left: 4px solid var(--gold) !important;
    border-radius: 18px 18px 18px 4px !important;
    box-shadow: 0 8px 20px rgba(26, 47, 74, 0.05) !important;
}

.chat-input textarea {
    border-radius: 16px !important;
    border: 1px solid rgba(26, 47, 74, 0.12) !important;
    background: #ffffff !important;
    font-size: 0.98rem !important;
    padding: 0.95rem 1rem !important;
}

.chat-input textarea:focus {
    border-color: rgba(201, 162, 39, 0.65) !important;
    box-shadow: 0 0 0 4px rgba(201, 162, 39, 0.12) !important;
}

.send-btn button {
    border-radius: 14px !important;
    background: linear-gradient(135deg, #c9a227, #a8841d) !important;
    color: #1a2f4a !important;
    font-weight: 700 !important;
    border: none !important;
    min-height: 48px !important;
    box-shadow: 0 10px 24px rgba(201, 162, 39, 0.28) !important;
}

.send-btn button:hover {
    filter: brightness(1.03);
    transform: translateY(-1px);
}

.clear-btn button {
    border-radius: 14px !important;
    background: transparent !important;
    color: var(--navy) !important;
    border: 1px solid rgba(26, 47, 74, 0.14) !important;
}

.footer-note {
    text-align: center;
    color: #7b8794;
    font-size: 0.82rem;
    margin-top: 0.8rem;
    padding-bottom: 0.4rem;
}

.footer-note strong {
    color: var(--navy);
}

@media (max-width: 900px) {
    .hero-shell {
        padding: 1.6rem 1.4rem 1.4rem;
    }
}
"""

HERO_HTML = """
<div class="hero-shell">
  <div class="hero-kicker">✦ Student Support · AI Assistant</div>
  <h1 class="hero-title">Your campus questions, answered with care.</h1>
  <p class="hero-subtitle">
    A conversational guide for admissions, scholarships, enrollment, and student
    services — grounded in university FAQs and powered by open-source AI.
  </p>
  <div class="hero-badge-row">
    <span class="hero-badge">Admissions</span>
    <span class="hero-badge">Financial Aid</span>
    <span class="hero-badge">Academic Programs</span>
    <span class="hero-badge">Student Services</span>
  </div>
</div>
"""

SIDEBAR_HTML = """
<div class="panel-card">
  <h2 class="panel-title">How it works</h2>
  <p class="panel-copy">
    Ask a question in plain language. The assistant retrieves relevant FAQ
    entries, then composes a clear response with cited sources.
  </p>
  <div class="topic-list">
    <div class="topic-item"><span class="topic-dot"></span><span class="topic-label">Semantic FAQ search</span></div>
    <div class="topic-item"><span class="topic-dot"></span><span class="topic-label">Grounded AI responses</span></div>
    <div class="topic-item"><span class="topic-dot"></span><span class="topic-label">Source transparency</span></div>
    <div class="topic-item"><span class="topic-dot"></span><span class="topic-label">Runs locally & open-source</span></div>
  </div>
</div>
"""

FOOTER_HTML = """
<div class="footer-note">
  Built for <strong>MSAI-631 Human-Computer Interaction</strong> ·
  Hugging Face + Gradio + RAG
</div>
"""

EXAMPLE_QUESTIONS = [
    "What are the admission requirements?",
    "How do I apply for financial aid?",
    "When is the scholarship application deadline?",
    "How do I register for classes?",
    "What student support services are available?",
]


def build_theme() -> gr.Theme:
    return gr.themes.Soft(
        primary_hue=gr.themes.colors.blue,
        secondary_hue=gr.themes.colors.amber,
        neutral_hue=gr.themes.colors.slate,
        font=[gr.themes.GoogleFont("Outfit"), "system-ui", "sans-serif"],
        font_mono=[gr.themes.GoogleFont("JetBrains Mono"), "monospace"],
    ).set(
        body_background_fill="#eef2f7",
        block_background_fill="transparent",
        block_border_width="0px",
        block_title_text_weight="600",
        button_primary_background_fill="#c9a227",
        button_primary_text_color="#1a2f4a",
        button_secondary_background_fill="#ffffff",
        input_background_fill="#ffffff",
    )
