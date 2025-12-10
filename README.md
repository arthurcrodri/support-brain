# Support Brain 🧠

**Support Brain** is an intelligent RAG (Retrieval-Augmented Generation) system designed to assist technical support operations. It ingests technical manuals (PDFs), processes them using data engineering best practices, and uses Generative AI to answer user queries with high accuracy.

## 🎯 Objective
This project was developed to demonstrate full-stack AI engineering capabilities, specifically targeting:
- **Data Engineering:** PDF processing, chunking strategies, and cleaning using `pandas`.
- **AI Integration:** Embedding generation and semantic search using **Gemini API** and **ChromaDB**.
- **Scalable Architecture:** Modular backend with FastAPI and modern frontend with Next.js.

## 🛠️ Tech Stack

### Backend & AI
- **Language:** Python 3.11+
- **API Framework:** FastAPI
- **Data Processing:** Pandas, NumPy (Data cleaning & Analytics)
- **Vector Store:** ChromaDB
- **LLM:** Google Gemini 1.5 Flash/Pro
- **Orchestration:** Custom RAG Logic (No abstraction frameworks, for total control)

### Frontend
- **Framework:** Next.js 14 (App Router)
- **Styling:** TailwindCSS
- **State:** React Hooks

## 📂 Architecture

The project follows a modular layered architecture to ensure separation of concerns:

```text
support-brain/
├── backend/            # API & AI Logic
│   ├── src/services/   # Business Logic (Ingestion, RAG, Vector Search)
│   ├── src/api/        # Routes & Controllers
│   └── notebooks/      # Data Analysis & Prototyping
└── frontend/           # User Interface
```

## 🚀 Getting Started

_Will be added in the future_
