import boto3
from app.utils.similarity import cosine_similarity

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("documents-dev")


def retrieve_top_k_chunks(
    query_embedding: list[float],
    top_k: int = 3,
):
    """
    Brute-force scan (OK for MVP / demo)
    """
    response = table.scan()
    items = response.get("Items", [])

    scored = []

    for item in items:
        emb = item.get("embedding")
        if not emb:
            continue

        score = cosine_similarity(query_embedding, emb)

        scored.append(
            {
                "document_id": item["document_id"],
                "filename": item["filename"],
                "chunk_id": item["chunk_id"],
                "score": score,
                "text": item["text"],
            }
        )

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:top_k]
