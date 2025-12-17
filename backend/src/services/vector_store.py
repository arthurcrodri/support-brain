import os
import chromadb
import pandas as pd
import google.generativeai as genai
from typing import List, Dict, Any
from chromadb.config import Settings

class VectorDB:
    """
        Manages the Vector Database (ChromaDB) interactions, including embedding generation using Google's Gemini API.
    """
    def __init__(self, collection_name: str = "technical_manuals"):
        print("--- DEBUG: Starting VectorDB ---")
        self.collection_name = collection_name
        self.api_key = os.getenv("GEMINI_API_KEY")
        
        if self.api_key:
            print(f"--- DEBUG: API Key found (ends in ...{self.api_key[-4:]})")
        else:
            print("--- DEBUG: CRITICAL ERROR - API Key is None! ---")
            raise ValueError("GEMINI_API_KEY not found on .env")

        print("--- DEBUG: Configuring GenAI... ---")
        genai.configure(api_key=self.api_key)
        
        # Initializing Persistent Client (saving data to disk)
        db_path = os.path.join(os.path.dirname(__file__), "../../data/chroma_db")
        print(f"--- DEBUG: ChromaDB path: {db_path}")
        self.client = chromadb.PersistentClient(path=db_path)
        
        # Getting or creating collection
        self.collection = self.client.get_or_create_collection(name=collection_name)
        print("--- DEBUG: VectorDB initialized successfully! ---")
        
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
            Generates embeddings for a batch of texts using Google Gemini model.
        """
        model = "models/embedding-001"
        results = genai.embed_content(
            model=model,
            content=texts,
            task_type="retrieval_document"
        )
        return results['embedding']

    def add_documents(self, df: pd.DataFrame, batch_size: int = 100):
        """
            Ingests a DataFrame of text chunks into the Vector Database.
        """
        if df.empty:
            print("No documents to add.")
            return
        
        total_chunks = len(df)
        print(f"Starting ingestion of {total_chunks} chunks into ChromaDB...")
        
        # Process in batches
        for i in range(0, total_chunks, batch_size):
            batch = df.iloc[i : i + batch_size]
            
            # Preparing data for Chroma
            ids = batch['id'].tolist()
            documents = batch['text'].tolist()
            metadatas = batch[['source', 'page', 'char_count']].to_dict('records')
            
            # Generating embeddings (calls Google API)
            try:
                embeddings = self._generate_embeddings(documents)
                
                # Upsert (update or insert)
                self.collection.upsert(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
                print(f"Processed batch {i} to {min(i + batch_size, total_chunks)}")
            except Exception as e:
                print(f"Error processing batch {i}: {e}")
                raise e
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
            Performs semantic search for a user query
        """
        # Embedding the query
        try:
            print(f"--- DEBUG: Searching for '{query}' ---")
            query_embedding = genai.embed_content(
                model="models/embedding-001",
                content=query,
                task_type="retrieval_query"
            )['embedding']
            
            # Querying ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Formatting results
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        "content": results['documents'][0][i],
                        "metadata": results['metadatas'][0][i],
                        "distance": results['distances'][0][i] if results['distances'] else None
                    })
            
            return formatted_results
        except Exception as e:
            print(f"Search error: {e}")
            return []

if __name__ == "__main__":
    # Smoke Test logic to verify imports and client initialization
    try:
        # Mock API Key if not present just for class instantiation test
        if not os.getenv("GEMINI_API_KEY"):
            os.environ["GEMINI_API_KEY"] = "TEST_KEY"
            print("WARNING: Using dummy API KEY for smoke test.")
        vdb = VectorDB()
        print("VectorDB Service initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
