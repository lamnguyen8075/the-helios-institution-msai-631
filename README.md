# University Student Support Chatbot

AI-powered university student support chatbot built for the MSAI-631 Human-Computer Interaction group project.

The chatbot answers common student questions about admissions, academic programs, scholarships, financial aid, enrollment, and student services using retrieval-augmented generation (RAG) and a custom React interface.

## Technologies

| Technology | Purpose |
|---|---|
| Python 3.11 | Backend and AI pipeline |
| FastAPI | REST API for chat requests |
| React + Tailwind CSS | Custom aesthetic UI |
| Hugging Face Transformers | Open-source language model |
| sentence-transformers | Semantic embeddings for retrieval |
| FAISS | Vector similarity search |
| PyTorch | Model runtime |

## Project Structure

```
MSAI-631-final/
├── server.py              # FastAPI server + static frontend hosting
├── pyproject.toml         # Python dependencies (uv)
├── frontend/              # React UI
│   └── src/
├── data/faq.json          # Curated university FAQ dataset
└── src/
    ├── service.py         # Shared chat service
    ├── retriever.py       # RAG retrieval
    └── chatbot.py         # Answer generation
```

## How It Works

1. The student asks a question in the React chat UI.
2. The frontend sends the message to `POST /api/chat`.
3. The question is embedded with `sentence-transformers`.
4. FAISS retrieves the most relevant FAQ entries.
5. Retrieved context is passed to an open-source Hugging Face model.
6. The UI displays the answer with cited sources.

## Setup and Run

### Production (one command after build)

```bash
cd frontend && npm install && npm run build && cd ..
uv run chatbot
```

Open **http://127.0.0.1:8000**

### Development (hot reload UI)

Terminal 1 — API:

```bash
uv run chatbot
```

Terminal 2 — React dev server:

```bash
cd frontend
npm install
npm run dev
```

Open **http://127.0.0.1:5173**

## Model Notes

- **Embeddings:** `sentence-transformers/all-MiniLM-L6-v2`
- **Generation:** `google/flan-t5-base` (lightweight, laptop-friendly)

## Team Roles

| Member | Role |
|---|---|
| Durga Ravichandra Malisetty | Project Lead / FAQ Curation |
| Aira Bhaima Shrestha | QA / Model Integration |
| Asif Ansari | Presentation Lead |
| Huy Lam Nguyen | React UI / UX Flow |
| Joanna Trautman | Presentation Design |
| Manindra Reddy Bhavanam | Python Implementation |
| Sinza Shrestha | Documentation Lead |

## Course Compliance

- Open-source only (no OpenAI or paid APIs)
- Runs locally on a standard laptop
- Demonstrates HCI through a conversational interface
- Uses Hugging Face as required by the course

## Attribution

Built as an extension of common Hugging Face chatbot patterns. RAG pipeline, FastAPI backend, and React UI were developed for this project.
