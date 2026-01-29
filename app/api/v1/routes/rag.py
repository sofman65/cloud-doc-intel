from fastapi import APIRouter
from app.schemas.rag import RagQueryRequest, RagQueryResponse
from app.services.rag.retrieval_service import retrieve_top_k_chunks
from app.services.rag.embedding_service import embed_text
from app.services.rag.answer_service import generate_answer

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/query", response_model=RagQueryResponse)
def rag_query(payload: RagQueryRequest):
    query_embedding = embed_text(payload.query)

    sources = retrieve_top_k_chunks(
        query_embedding=query_embedding,
        top_k=payload.top_k,
    )

    answer = generate_answer(
        query=payload.query,
        sources=sources,
    )

    return {
        "answer": answer,
        "sources": [
            {
                "document_id": s["document_id"],
                "filename": s["filename"],
                "chunk_id": s["chunk_id"],
                "score": s["score"],
                "text_snippet": s["text"][:300],
            }
            for s in sources
        ],
        "meta": {
            "model": "claude-3-sonnet",
            "top_k": payload.top_k,
        },
    }
