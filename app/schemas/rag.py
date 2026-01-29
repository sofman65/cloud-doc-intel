from pydantic import BaseModel, Field
from typing import List, Optional
from uuid import UUID


class RagFilters(BaseModel):
    document_ids: Optional[List[UUID]] = None
    content_type: Optional[str] = None


class RagQueryRequest(BaseModel):
    query: str = Field(..., min_length=1)
    top_k: int = Field(default=3, ge=1, le=10)
    filters: Optional[RagFilters] = None


class RagSource(BaseModel):
    document_id: UUID
    filename: str
    chunk_id: str
    score: float
    text_snippet: str


class RagQueryResponse(BaseModel):
    answer: str
    sources: List[RagSource]
    meta: dict
