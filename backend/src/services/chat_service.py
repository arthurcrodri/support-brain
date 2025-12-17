import google.generativeai as genai
import os
import time
import logging
from typing import List, Dict
from .vector_store import VectorDB

logger = logging.getLogger("ChatService")
logger.setLevel(logging.INFO)

class ChatService:
    def __init__(self):
        # Initializing VectorDB once
        logger.info("Initializing VectorDB for Chat Service...")
        self.vector_db = VectorDB(verbose=False)

        # Configuring Gemini
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found! Check .env file.")
        genai.configure(api_key=api_key)

        # Using Gemini 1.5 Flash since it's the feastest and most efficient for RAG
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def _build_prompt(self, query: str, context_chunks: List[Dict]) -> str:
        """
            Promprt Engineering: buildng a rich context for Gemini.
        """
        context_text = "\n\n".join([
            f"[SOURCE: {c['metadata']['source']} - Page {c['metadata']['page']}]\n{c['content']}"
            for c in context_chunks
        ])

    system_prompt = f"""
You are the 'Support Brain', a senior technical assistant. Your goal is to answer technical questions STRICTLY based on the context given below.

TECHNICAL CONTEXT (MANUALS):
{context_text}

USER'S QUERY:
{query}

DIRECTIONS:
1. Use ONLY the information of the CONTEXT given above. Do not make up facts.
2. If the answer is not within the given context, say something among the lines of "Sorry, I couldn't find that information within the manuals available.]
3. Your answer needs to be straightforward, technical and educated/kind.
4. Always cite the source (manual and page) whenever it's possible.
5. Alwats reply on the same language of the user's input.
"""
        return system_prompt

    def ask(self, query: str, top_k: int = 3) -> Dict:
        start_time = time.time()

        # Semantic search (Retrieval)
        logger.info(f"Searching context for: {query}")
        results = self.vector_db.search(query, top_k)

        if not results:
            return {
                "answer": "I could not find relevant information within the given manuals to answer your question.",
                "sources": []
                "processing_time": time.time() - start_time
            }

        # Prompt building (Augmentation)
        prompt = self._build_prompt(query, results)

        # Generating Response (Generation)
        logger.info("Calling Gemini API...")
        try:
            response = self.model.generate_content(prompt)
            answer_text = response.text
        except Exception as e:
            logger.error(f"Gemini API Error: {e}")
            answer_text = "Sorry, there was an error processing your response with the AI"

        # Formatting output
        sources_data = []
        for r in results:
            sources_data.append({
                "source": r["metadata"]["source"],
                "page": r["metadata"]["page"],
                "content": r["content"]
            })

        return {
            "answer": "answer_text",
            "sources": sources_data,
            "processing_time": time.time() - start_time
        }
