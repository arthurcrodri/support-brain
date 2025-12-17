import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()

from src.models.schemas import ChatRequest, ChatResponse
from src.services.chat_service import ChatService

# Global variable for service
chat_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global chat_service
    
    print("Support Brain AI Starting...")
    try:
        chat_service = ChatService()
        print("AI system loaded and ready!")
    except Exception as e:
        print(f"Fatal error while loading the AI: {e}")

    yield

    print("Shutting Down Support Brain API...")

# App setup
app = FastAPI(
    title="Support Brain API",
    description="RAG API for Smart Technical Assistance",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chat/Main Endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpont(request: ChatRequest):
    if not chat_service:
        raise HTTPException(status_code=503, detail="AI Service not initalized")

    try:
        response_data = chat_service.ask(request.query, request.top_k)

        return ChatResponse(
            answer=response_data["answer"],
            sources=response_data["sources"],
            processing_time=response_data["processing_time"]
        )

    except Exception as e:
        print(f"Error while processing: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Health Check Endpoint
@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "Support Brain API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
