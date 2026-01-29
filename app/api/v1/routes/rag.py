from fastapi import APIRouter
from uuid import UUID
from app.schemas.rag import (
    RagQueryRequest,
    RagQueryResponse,
    RagSource,
)

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post(
    "/query",
    response_model=RagQueryResponse,
    summary="RAG query (stub)",
)
async def rag_query_stub(payload: RagQueryRequest):
    """
    Stub RAG endpoint.
    Returns a fake answer and fake sources.
    """

    fake_sources = [
        RagSource(
            document_id=UUID("b64d51c6-cca9-4ab3-8ce8-e0892feac63c"),
            filename="ΠΤΥΧΙΟ.pdf",
            chunk_id="CHUNK#0003",
            score=0.91,
            text_snippet="This degree was awarded to Sofianos Lampropoulos...",
        ),
        RagSource(
            document_id=UUID("46a13f52-219b-4e0d-8a9f-7718f0ab5a20"),
            filename="ΠΤΥΧΙΟ.pdf",
            chunk_id="CHUNK#0001",
            score=0.87,
            text_snippet="The curriculum includes Electrical and Computer Engineering courses...",
        ),
    ]

    return RagQueryResponse(
        answer=f"Stub answer for query: '{payload.query}'",
        sources=fake_sources[: payload.top_k],
        meta={
            "model": "stub",
            "embedding_model": "stub",
            "latency_ms": 42,
        },
    )
