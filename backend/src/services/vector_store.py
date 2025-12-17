import os
import logging
import chromadb
import pandas as pd
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer

logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class VectorDB:
    """
        Manages the Vector Database (ChromaDB) interactions using Local Embeddings (Sentence-Transformers)
    """
    def __init__(self, collection_name: str = "technical_manuals", verbose: bool = False):
        self.logger = logging.getLogger("VectorDB")
        if verbose:
            self.logger.setLevel(logging.DEBUG)
        else:
            self.logger.setLevel(logging.INFO)

        self.logger.debug("--- Starting VectorDB Initialization ---")
        self.logger.info("Loading local embedding model (all-MiniLM-L6-v2)...")
        try:
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2', device='cpu')
        except Exception as e:
            self.logger.warning(f"Network error({e}). Loading model from LOCAL CACHE only.")
            self.embedding_model = SetenceTransformer('all-MiniLM-L6-v2', device='cpu', local_files_only=True)

        db_path = os.path.join(os.path.dirname(__file__), "../../data/chroma_db")

        if not verbose:
            logging.getLogger("chromadb").setLevel(logging.ERROR)

        self.client = chromadb.PersistentClient(path=db_path)
        self.collection = self.client.get_or_create_collection(name=collection_name)
        self.logger.info("--- VectorDB Service initialized successfully! ---")
        
    def _generate_embeddings(self, texts: List[str]) -> List[List[float]]:
        """
            Generates embeddings locally.
        """
        embeddings = self.embedding_model.encode(texts)

        if len(embeddings.shape) == 1:
            embeddings = embeddings.reshape(1, -1)
        
        return embeddings.tolist()

    def add_documents(self, df: pd.DataFrame, batch_size: int = 50):
        """
            Ingests a DataFrame of text chunks into the Vector Database.
        """
        if df.empty:
            self.logger.warning("No documents to add.")
            return
        
        total_chunks = len(df)
        self.logger.info(f"Starting ingestion of {total_chunks} chunks into ChromaDB...")
        
        # Process in batches
        for i in range(0, total_chunks, batch_size):
            batch = df.iloc[i : i + batch_size]
            
            # Preparing data for Chroma
            ids = batch['id'].tolist()
            documents = batch['text'].tolist()
            metadatas = batch[['source', 'page', 'char_count']].to_dict('records')
            
            # Generating embeddings locally
            try:
                embeddings = self._generate_embeddings(documents)
                
                # Upsert (update or insert)
                self.collection.upsert(
                    ids=ids,
                    documents=documents,
                    embeddings=embeddings,
                    metadatas=metadatas
                )
                self.logger.debug(f"Processed batch {i} to {min(i + batch_size, total_chunks)}")
            except Exception as e:
                self.logger.error(f"Error processing batch {i}: {e}")
                raise e

        self.logger.info("Ingestion completed.")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """
            Performs semantic search for a user query
        """
        
        # Embedding the query
        try:
            self.logger.debug(f"Searching for '{query}'")
            query_embeddings = self._generate_embeddings([query])

            query_vector = query_embeddings[0]

            # Querying ChromaDB
            results = self.collection.query(
                query_embeddings=[query_vector],
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
            self.logger.error(f"Search error: {e}")
            return []

if __name__ == "__main__":
    # Smoke Test logic to verify imports and client initialization
    try:
        vdb = VectorDB()
        print("Local VectorDB Service initialized successfully.")
    except Exception as e:
        print(f"Initialization failed: {e}")
