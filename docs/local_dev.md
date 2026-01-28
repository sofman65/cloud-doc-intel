# Local Development Guide (local_dev.md)

This document describes how to run **Cloud Doc Intel Backend** locally in a production-like way.

The goal is:
- fast iteration
- minimal AWS friction
- same codebase as production
- clear separation between *local* and *cloud*

---

## 1. Prerequisites

### Required
- Python 3.11
- Docker + Docker Desktop
- AWS CLI v2
- Git

### Optional but Recommended
- virtualenv / venv
- Postman or HTTPie
- Terraform (for infra parity)

---

## 2. Repository Structure (Relevant Parts)

```
DocIntelBackend/
├── app/
│   ├── api/
│   ├── services/
│   ├── core/
│   └── main.py
├── terraform/
├── Dockerfile
├── requirements.txt
├── .env.local
└── README.md
```

---

## 3. Environment Configuration

Local development uses **.env.local**.

Example:

```env
APP_ENV=local
LOG_LEVEL=DEBUG

AWS_REGION=us-east-1
AWS_DEFAULT_REGION=us-east-1

S3_BUCKET_NAME=cloud-doc-intel-dev
S3_PREFIX=documents/

DYNAMODB_TABLE_NAME=documents-dev

ENABLE_AI=false
ENABLE_AUTH=false
```

### Important
- `.env.local` is **not committed**
- AWS credentials are resolved via:
  - `aws configure`
  - or environment variables
  - or IAM role (when running in cloud)

---

## 4. Python (Local, No Docker)

### Create virtual environment
```bash
python3.11 -m venv venv
source venv/bin/activate
```

### Install dependencies
```bash
pip install -r requirements.txt
```

### Run the API
```bash
uvicorn app.main:app --reload
```

### Health check
```bash
curl http://127.0.0.1:8000/api/v1/health
```

Expected:
```json
{ "status": "ok", "env": "local" }
```

---

## 5. Docker (Local, Production-like)

### Build image
```bash
docker build -t doc-intel-backend .
```

### Run container
```bash
docker run --rm -p 8000:8000 \
  -e AWS_REGION=us-east-1 \
  -e S3_BUCKET_NAME=cloud-doc-intel-dev \
  -e S3_PREFIX=documents/ \
  -e DYNAMODB_TABLE_NAME=documents-dev \
  doc-intel-backend
```

### Why Docker locally?
- Same runtime as ECS
- Catches dependency & OS issues early
- Avoids "works on my machine" bugs

---

## 6. AWS Usage in Local Mode

### S3
- Real S3 bucket is used
- Files are uploaded exactly as in production
- No local filesystem mocking

### DynamoDB
- Real DynamoDB table
- PAY_PER_REQUEST billing
- Simple primary key access

### Why not LocalStack?
**Deliberate choice**:
- Matches real AWS behavior
- Fewer false positives
- Better production confidence

---

## 7. API Endpoints to Test Locally

### Upload
```
POST /api/v1/upload
```

### List documents
```
GET /api/v1/documents
```

### Get document
```
GET /api/v1/documents/{document_id}
```

### Download (presigned URL)
```
GET /api/v1/documents/{document_id}/download
```

---

## 8. Common Local Issues

### 1. AWS Permission Errors
Cause:
- IAM user lacks permissions

Fix:
- Attach policies for:
  - S3
  - DynamoDB
  - (later) ECR / ECS

---

### 2. Region Mismatch
Cause:
- Different region in:
  - AWS CLI
  - `.env.local`
  - Terraform

Fix:
- Standardize on **us-east-1**

---

### 3. Docker on Apple Silicon
Cause:
- ARM vs AMD64 mismatch

Fix:
```bash
docker buildx build --platform linux/amd64 -t doc-intel-backend .
```

---

## 9. Local vs Production Parity

| Concern        | Local | Production |
|---------------|------|------------|
| FastAPI app   | ✅   | ✅ |
| Docker image  | ✅   | ✅ |
| S3            | ✅   | ✅ |
| DynamoDB      | ✅   | ✅ |
| IAM           | User | Role |
| ALB / ECS     | ❌   | ✅ |


