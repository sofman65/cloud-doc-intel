variable "project_name" {
  type        = string
  description = "Project name"
}

variable "environment" {
  type        = string
  description = "Environment name (dev, prod)"
}

variable "aws_region" {
  type        = string
  default     = "us-east-1"
}

variable "ecr_image_url" {
  type = string
  description = "ECR image URI for the backend service"
}

