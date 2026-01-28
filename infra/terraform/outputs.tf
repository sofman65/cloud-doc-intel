output "s3_bucket_name" {
  value       = aws_s3_bucket.documents.bucket
  description = "S3 bucket used for document storage"
}


output "dynamodb_table_name" {
  value       = aws_dynamodb_table.documents.name
  description = "DynamoDB table for document metadata"
}
