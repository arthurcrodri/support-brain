# 🧠 Support Brain AI

> **Intelligent Technical Support Assistant powered by RAG (Retrieval-Augmented Generation) and Google Gemini 2.5.**

![Project Status](https://img.shields.io/badge/status-active-success.svg)
![Stack](https://img.shields.io/badge/stack-Next.js_15_|_FastAPI_|_Gemini_AI-blue)
![License](https://img.shields.io/badge/license-MIT-green)

## 📖 About the Project

**Support Brain** is a Full Stack AI application designed to solve complex technical support scenarios. Unlike generic chatbots, Support Brain uses a **RAG (Retrieval-Augmented Generation)** architecture to "read" specific technical manuals (PDFs), index their content, and provide accurate, context-aware answers with citations.

It was built to assist technicians and users in troubleshooting hardware errors (e.g., Dell Servers) by retrieving exact procedures from official documentation.

## ✨ Key Features

* **RAG Architecture:** Ingests and chunks PDF manuals for semantic search.
* **Vector Database:** Uses **ChromaDB** with local embeddings (`all-MiniLM-L6-v2`) for privacy and speed.
* **LLM Integration:** Powered by **Google Gemini 2.5 Flash** for high-speed, reasoning-heavy responses.
* **Citation System:** Every answer includes references to the specific file and page number used.
* **Modern Frontend:** Built with **Next.js 15**, **TypeScript**, and **Tailwind CSS v4**.
* **Dark Mode UI:** Sleek, developer-focused interface inspired by modern AI tools.

## 🛠️ Tech Stack

### **Frontend**
* **Framework:** Next.js 15 (App Router)
* **Language:** TypeScript
* **Styling:** Tailwind CSS (v4) + Lucide React (Icons)
* **State:** React Hooks
* **HTTP Client:** Axios

### **Backend**
* **Framework:** FastAPI (Python 3.12+)
* **Vector DB:** ChromaDB
* **LLM Orchestration:** Google Generative AI SDK
* **Embeddings:** SentenceTransformers (`sentence-transformers/all-MiniLM-L6-v2`)
* **PDF Processing:** PyPDF

## 🚀 How It Works

1.  **Ingestion:** The system loads technical manuals (PDFs) from the `data/` directory.
2.  **Embedding:** Text is split into chunks and converted into vector embeddings using a local model.
3.  **Retrieval:** When a user asks a question, the system searches the VectorDB for the most relevant chunks.
4.  **Generation:** The relevant context + the user query are sent to **Gemini 2.5**.
5.  **Response:** The AI generates an answer based *only* on the provided context, citing sources.

## 📦 Getting Started

### Prerequisites
* Node.js 18+
* Python 3.10+
* A Google Gemini API Key

### 1. Clone the Repository
```bash
git clone https://github.com/arthurcrodri/support-brain.git
cd support-brain
```

### 2. Backend Setup

Navigate to the backend folder and set up the Python environment.

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install fastapi uvicorn google-generativeai chromadb pypdf sentence-transformers python-dotenv

# Set up Environment Variables
# Create a .env file and add your Google API Key:
echo "GOOGLE_API_KEY=your_api_key_here" > .env

# Run the Server
python main.py
```

_The backend runs on `http://localhost:8000`_

### 3. Frontend Setup

Open a new terminal and navigate to the frontend folder.

```bash
cd frontend

# Install dependencies
npm install

# Run the Development Server
npm run dev
```

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the ![issues page](https://github.com/arthurcrodri/support-brain/issues)

# 📝 License

This project is ![MIT](LICENSE) licensed.

---

Developed by **Arthur Rodrigues** (arthur.rodrigues.dev@proton.me)

Computer Engineering Student at UFRN

2025.
