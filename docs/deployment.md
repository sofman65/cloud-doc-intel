# Deployment Guide

This document describes how the **Cloud Doc Intel Backend** is built,
deployed, and run in production on AWS.

The deployment follows a **container-first, Infrastructure-as-Code**
approach using Docker, Amazon ECR, ECS Fargate, and Terraform.

------------------------------------------------------------------------

## Deployment Overview

The backend is deployed as a Docker container running on **AWS ECS
Fargate**, fronted by an **Application Load Balancer (ALB)**.

High-level flow:

1.  Build Docker image locally
2.  Push image to Amazon ECR
3.  Provision infrastructure with Terraform
4.  ECS pulls the image and starts the service
5.  ALB routes traffic to healthy tasks

------------------------------------------------------------------------

## Prerequisites

-   AWS account with sufficient IAM permissions
-   Docker (with Buildx enabled)
-   Terraform ≥ 1.5
-   AWS CLI configured
-   Amazon ECR repository created

------------------------------------------------------------------------

## Step 1: Build the Docker Image

The backend is packaged as a Docker image using the provided
`Dockerfile`.

### Important: Platform Architecture

When building on Apple Silicon (M1/M2/M3), Docker defaults to
`linux/arm64`.\
AWS ECS Fargate expects `linux/amd64`.

The image **must** be built explicitly for `linux/amd64`.

### Build command

``` bash
docker buildx build \
  --platform linux/amd64 \
  -t doc-intel-backend:latest \
  .
```

------------------------------------------------------------------------

## Step 2: Push Image to Amazon ECR

Authenticate Docker with ECR:

``` bash
aws ecr get-login-password --region us-east-1 \
| docker login --username AWS --password-stdin \
533267307199.dkr.ecr.us-east-1.amazonaws.com
```

Tag the image:

``` bash
docker tag doc-intel-backend:latest \
533267307199.dkr.ecr.us-east-1.amazonaws.com/doc-intel-backend:latest
```

Push to ECR:

``` bash
docker push \
533267307199.dkr.ecr.us-east-1.amazonaws.com/doc-intel-backend:latest
```

------------------------------------------------------------------------

## Step 3: Infrastructure Provisioning (Terraform)

All infrastructure is defined under the `infra/` directory and managed
using Terraform.

### Resources Provisioned

Terraform creates and manages:

-   S3 bucket (document storage)
-   DynamoDB table (document metadata)
-   ECS cluster
-   ECS task definition
-   ECS service (Fargate)
-   Application Load Balancer
-   Target group and listener
-   IAM roles and policies
-   CloudWatch log group

### Apply Infrastructure

``` bash
terraform init
terraform plan
terraform apply
```

Terraform outputs include:

-   ALB public URL
-   S3 bucket name
-   DynamoDB table name

------------------------------------------------------------------------

## Step 4: ECS Service Startup

After Terraform applies:

-   ECS creates a new task definition revision
-   ECS starts one or more Fargate tasks
-   Tasks register their ENI IPs with the ALB target group
-   ALB health checks `/api/v1/health`

Once healthy, traffic is routed to the service.

------------------------------------------------------------------------

## Step 5: Verification

### Health Check

``` bash
curl http://<alb_url>/api/v1/health
```

Expected response:

``` json
{"status":"ok","env":"dev"}
```

### Upload Test

``` bash
curl -X POST \
  http://<alb_url>/api/v1/upload \
  -F "file=@test.pdf"
```

Verify:

-   File exists in S3
-   Metadata exists in DynamoDB
-   API returns a document ID

