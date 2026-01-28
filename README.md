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

```mermaid
flowchart TB
    CLIENT["Client
(Browser / API Consumer)"]

    APIGW["API Gateway
HTTP / REST"]

    LAMBDA["AWS Lambda
FastAPI (ASGI)
Mangum Adapter"]

    ROUTES["API Routes
/api/v1/*
Validation & HTTP"]

    SERVICES["Services Layer
Business Logic
AWS Integrations"]

    S3["Amazon S3
Document Storage"]

    DDB["DynamoDB
Metadata / Index"]

    AI["Optional AI Layer
Bedrock / Textract"]

    CW["CloudWatch
Logs & Metrics"]

    CLIENT --> APIGW
    APIGW --> LAMBDA

    LAMBDA --> ROUTES
    ROUTES --> SERVICES

    SERVICES --> S3
    SERVICES --> DDB
    SERVICES --> AI

    LAMBDA --> CW
```
