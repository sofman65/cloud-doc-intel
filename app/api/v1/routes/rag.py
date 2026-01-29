from fastapi import APIRouter
from app.schemas.rag import RagQueryRequest, RagQueryResponse, RagSource
from app.services.rag.retrieval_service import retrieve_top_k_chunks
from app.services.rag.embedding_service import embed_text

router = APIRouter(prefix="/rag", tags=["RAG"])


@router.post("/query", response_model=RagQueryResponse)
async def rag_query(payload: RagQueryRequest):
    query_embedding = embed_text(payload.query)

    chunks = retrieve_top_k_chunks(
        query_embedding=query_embedding,
        top_k=payload.top_k,
    )

    sources = [
        RagSource(
            document_id=chunk["document_id"],
            filename=chunk["filename"],
            chunk_id=chunk["chunk_id"],
            score=round(chunk["score"], 4),
            text_snippet=chunk["text"][:300],
        )
        for chunk in chunks
    ]

    combined_context = "\n\n".join(f"- {c['text']}" for c in chunks)

    return RagQueryResponse(
        answer=f"Retrieved context:\n{combined_context}",
        sources=sources,
        meta={
            "retriever": "dynamodb-scan",
            "similarity": "cosine",
            "top_k": payload.top_k,
        },
    )
