import sys
import os
from dotenv import load_dotenv

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

env_path = os.path.join(os.path.dirname(__file__), '../backend/.env')
load_dotenv(env_path)

if not os.getenv("GEMINI_API_KEY"):
    print("ERROR: GEMINI_API_KEY not found")
    print(f"Please make sure to create the file at: {os.path.abspath(env_path)}")
    print("Expected content: GEMINI_API_KEY=your_key_here")
    sys.exit(1)

from src.services.ingestion import PDFProcessor
from src.services.vector_store import VectorDB

def run_pipeline():
    print("--- STARTING FULL RAG PIPELINE TEST ---")

    # Defining paths
    pdf_path = "backend/data/manuals/manual_generico.pdf"

    # Ingestion
    print(f"\n[1/3] Processing PDF: {pdf_path}...")
    processor = PDFProcessor(chunk_size=300, overlap=50)
    try:
        df = processor.process(pdf_path)
        print(f"Success! {len(df)} chunks generated.")
    except FileNotFoundError:
        print("PDF not found. Please run 'python backend/create_dummy_pdf.py' first.")
        return

    # Indexing (vector store)
    print("\n[2/3] Generating Embeddings and saving on ChromaDB (consuming Google's API)...")
    try:
        vdb = VectorDB(collection_name="test_manuals")
        vdb.add_documents(df)
        print("Data indexed successfully!")
    except Exception as e:
        print(f"Indexing error: {e}")
        return

    # Retrieval
    query = "O que eu faço se o sistema der erro de temperatura?"

    print(f"[3/3] Testing semantic search...")
    print(f"Query: {query}")

    results = vdb.search(query, top_k=2)

    print("\n--- RESULTS FOUND ---")
    if results:
        for i, res in enumerate(results):
            print(f"\nResult {i+1} (Distance: {res['distance']:..4f}):")
            print(f"Source: {res['metadata']['source']} (Page {res['metadata']['page']})")
            print(f"Content: {res['content'].strip()}")
    else:
        print("No relevant results were found.")

if __name__ == "__main__":
    run_pipeline()
