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
  default     = "eu-west-1"
}
