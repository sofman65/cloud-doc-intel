# Cloud Doc Intel Backend

Production-grade document ingestion backend built with **FastAPI** and deployed on **AWS ECS Fargate**, designed to demonstrate real-world cloud engineering and deployment practices.

The service provides a scalable API for uploading, storing, and retrieving documents using AWS-native services.

---

## 🎯 What This Project Does

- Exposes a REST API for document upload and retrieval
- Stores raw files in **Amazon S3**
- Stores document metadata in **DynamoDB**
- Serves downloads via **presigned S3 URLs**
- Runs as a **containerized FastAPI service** behind an **Application Load Balancer**
- Infrastructure fully managed with **Terraform**

---

## 🚀 Tech Stack

### Backend
- FastAPI
- Uvicorn
- Pydantic

### AWS
- ECS Fargate (container runtime)
- Application Load Balancer (public entry point)
- S3 (document storage)
- DynamoDB (metadata storage)
- ECR (container registry)
- IAM (least-privilege access)
- CloudWatch (logs & metrics)

### Infrastructure
- Terraform (Infrastructure as Code)
- Docker (containerization)

---

## Local Development
See [docs/local-development.md](docs/local-dev.md)

## Deployment
See [docs/deployment.md](docs/deployment.md)

## 🧠 Architecture Overview

```mermaid
flowchart TB
    CLIENT["Client
(Browser / API Consumer)"]

    ALB["Application Load Balancer
HTTP :80"]

    ECS["ECS Fargate Service
FastAPI + Uvicorn"]

    ROUTES["API Routes
/api/v1/*"]

    SERVICES["Service Layer
Business Logic"]

    S3["Amazon S3
Document Storage"]

    DDB["Amazon DynamoDB
Document Metadata"]

    CW["CloudWatch
Logs & Metrics"]

    CLIENT --> ALB
    ALB --> ECS

    ECS --> ROUTES
    ROUTES --> SERVICES

    SERVICES --> S3
    SERVICES --> DDB

    ECS --> CW

