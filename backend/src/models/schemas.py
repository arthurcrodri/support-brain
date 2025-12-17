from pydantic import BaseModel
from typing import List, Optional

# Source/Citation
class SourceModel(BaseModel):
    source: str
    page: int
    content: str

# User Request
class ChatRequest(BaseModel):
    query: str
    top_k: int = 3

# System Response
class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceModel]
    processing_time: float    # Measuring latence
