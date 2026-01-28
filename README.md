# Cloud Doc Intel Backend

Production-style backend service built with **FastAPI** and **AWS**, designed to demonstrate real-world cloud engineering practices.

This project focuses on:
- clean architecture
- environment separation
- AWS-native integrations
- infrastructure as code

---

## 🚀 Tech Stack

**Backend**
- FastAPI
- Uvicorn
- Pydantic

**AWS**
- Lambda + API Gateway
- S3 (document storage)
- DynamoDB (metadata)
- IAM (least-privilege access)
- CloudWatch (logging)

**Infrastructure**
- Terraform (modular)
- GitHub Actions (CI/CD)

---

## 🧠 Architecture Overview

flowchart TD
    Client["Client<br/>(Browser / API Consumer)"]

    APIGW["API Gateway"]

    Lambda["AWS Lambda<br/>(FastAPI via Mangum)"]

    Routes["API Routes<br/>(/api/v1/*)"]
    Services["Services Layer<br/>(Business Logic)"]

    S3["Amazon S3<br/>(Document Storage)"]
    DynamoDB["DynamoDB<br/>(Metadata Store)"]
    Bedrock["(Optional)<br/>AWS Bedrock / Textract"]

    CloudWatch["CloudWatch<br/>(Logs & Metrics)"]

    Client --> APIGW
    APIGW --> Lambda
    Lambda --> Routes
    Routes --> Services

    Services --> S3
    Services --> DynamoDB
    Services --> Bedrock

    Lambda --> CloudWatch
