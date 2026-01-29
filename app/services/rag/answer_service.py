import boto3
import json
from typing import List

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
# Titan is embeddings-only; Claude is correct for generation


def generate_answer(
    query: str,
    sources: List[dict],
) -> str:
    """
    Generate a grounded answer using retrieved sources.
    """

    context_blocks = []
    for i, src in enumerate(sources, start=1):
        context_blocks.append(f"[Source {i} | {src['filename']}]\n{src['text']}")

    context = "\n\n".join(context_blocks)

    prompt = f"""
You are a retrieval-augmented assistant.

Rules:
- Answer ONLY using the provided sources
- If the answer is not contained in the sources, say: "I don't know based on the provided documents."
- Do NOT invent facts
- Be concise and factual

Question:
{query}

Sources:
{context}

Answer:
""".strip()

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(
            {
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.0,
            }
        ),
        contentType="application/json",
        accept="application/json",
    )

    body = json.loads(response["body"].read())
    return body["content"][0]["text"]
