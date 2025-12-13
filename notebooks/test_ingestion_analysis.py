import sys
import os
import pandas as pd

# Adding the backend root directory to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

from src.services.ingestion import PDFProcessor

def run_analysis():
    print("--- STARTING DATA INGESTION ANALYSIS ---")

    # Set up
    pdf_path = "backend/data/manuals/manual_generico.pdf"
    processor = PDFProcessor(chunk_size=200, overlap=50) # Small chunk for testing

    print(f"Target: {pdf_path}")

    # Pipeline Execution
    try:
        df = processor.process(pdf_path)
    except FileNotFoundError:
        print("ERROR: Generate the PDF first by running 'python backend/create_dummy_pdf.py'")
        return

    # Analysis with Pandas
    if not df.empty:
        print("\n[SUCCESS] DataFrame generated!")
        print("-" * 30)

        print("\nData Sample (Head):")
        print(df[['id', 'text', 'char_count']].head(3))

        print("\nDescriptive Statistics (Chunk Szie):")
        print(df['char_count'].describe())

        print("\n Overlap Check (Logic):")
        # Checks if the end of one chunk appears at the start of the next one
        chunk_0 = df.iloc[0]['text']
        chunk_1 = df.iloc[1]['text']
        print(f"Chunk 0 (last 50 chars): ...{chunk_0[-50]}")
        print(f"Chunk 1 (first 50 chars): {chunk_1[:50]}...")

    else:
        print("[WARNING] No data was extracted. Please check the PDF file.")

if __name__ == "__main__":
    run_analysis()
