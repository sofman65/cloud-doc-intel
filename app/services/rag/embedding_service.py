import boto3
import json

bedrock = boto3.client(
    service_name="bedrock-runtime",
    region_name="us-east-1",
)

MODEL_ID = "amazon.titan-embed-text-v2"


def embed_text(text: str) -> list[float]:
    """
    Generate embeddings using Amazon Titan via Bedrock
    """
    body = {"inputText": text}

    response = bedrock.invoke_model(
        modelId=MODEL_ID,
        body=json.dumps(body),
        accept="application/json",
        contentType="application/json",
    )

    response_body = json.loads(response["body"].read())

    return response_body["embedding"]
