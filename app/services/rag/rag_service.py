from app.services.rag.embedding_service import embed_text
from app.services.rag.retrieval_service import retrieve_top_k_chunks


def rag_query(query: str, top_k: int = 3, filters=None):
    query_embedding = embed_text(query)

    chunks = retrieve_top_k_chunks(
        query_embedding=query_embedding,
        top_k=top_k,
    )

    sources = [
        {
            "document_id": chunk["document_id"],
            "filename": chunk["filename"],
            "chunk_id": chunk["chunk_id"],
            "score": round(chunk["score"], 4),
            "text_snippet": chunk["text"][:300],  # 👈 safe snippet
        }
        for chunk in chunks
    ]

    return sources
