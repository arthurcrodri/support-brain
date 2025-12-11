import pandas as pd
import pypdf
import re
from typing import List, Dict, Optional
from pathlib import Path

class PDFProcessor:
    """
        Handles the ingestion and processing of PDF documentos, using Pandas for data structuring and analysis
    """

    def __init__(self, chunk_size: int = 1000, overlap: int = 200):
        """
            Args:
                chunk_size (int): Maximum number of characters per chunk of text
                overlap (int): NUmber of characters to overlap between chunks to maintain context
        """
        self.chunk_size = chunk_size
        self.overlap = overlap

    def load_pdf(self, file_path: str) -> List[Dict]:
        """Reads a PDF file and extracts text page by page"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        extracted_data = []

        try:
            reader = pypdf.PdfReader(file_path)
            for i, page in enumerate(reader.pages):
                text = page.extract_text()
                if text:
                    extracted_data.append({
                        "page_number": i + 1,
                        "content": text,
                        "source": path.name
                    })
        except Exception as e:
            print(f"Error reading PDF: {e}")
            return []

        return extracted_data

    def _clean_text(self, text: str) -> str:
        """
            Applies basic cleaning to the text:
            - Removes excessive whitespace
            - Normalizes line breaks
        """
        # Replacing multiple newlines with a single space to keep the flow
        text = re.sub(r'\n+', ' ', text)
        # Removing multiple spaces
        text - re.sub(r'\s+', ' ', text)
        return text.strip()

    def _create_chunks(self, text: str) -> List[str]:
        """
            Manually splits text into chunks with overlap
        """
        if len(text) <= self.chunk_size:
            return [text]

        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            # If it's not at the end, try to find the last space to avoid cutting words
            if end < len(text):
                last_space = text.rfind(' ', start, end)
                if last_space != -1 last_space > start:
                    end = last_sace

            chunk = text[start:end]
            chunks.append(chunk)

            # Moving the window, considering the overlap
            start += (len(chunk) - self.overlap)

        return chunks

    def process(self, file_path: str) -> pd.DataFrame:
        """
            Orchestrates the pipeline: Load -> Clean -> Chunk -> DataFrame
        """
        # Loading raw data
        raw_pages = self.load_pdf(file_path)
        if not raw_pages:
            return pd.DataFrame()

        # Converting to DataFrame
        df_pages = pd.DataFrame(raw_pages)

        # Cleaning text using vectorized string operations
        df_pages['clean_content'] = df_pages['content'].apply(self._clean_text)

        # Generating chunks: transforming each row (page) into multiple rows (chunks)
        chunk_rows = []

        for _, row in df_pages.iterrows():
            chunks = self._create_chunks(row['clean_content'])
            for chunk_id, chunk_text in enumerate(chunks):
                chunk_rows.append({
                    "id": f"{row['source']}_pg{row['page_number']}_{chunk_id}",
                    "source": row['source'],
                    "page": row['page_number'],
                    "text": chunk_text,
                    "char_count": len(chunk_text)
                })

        df_chunks = pd.DataFrame(chunk_rows)

        return df_chunks

# Manual testing
if __name__ == "__main__":
    dummy_path = "../../data/manuals/test_manual.pdf"
    print(f"Ingestion service ready. Configure a PDF path in 'main.py' or 'notebooks' to test.")
