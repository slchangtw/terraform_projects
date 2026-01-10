output "lambda_function_name" {
  description = "The name of the Lambda function"
  value       = aws_lambda_function.lambda.function_name
}

output "dynamodb_table_name" {
  description = "The name of the DynamoDB table for idempotency"
  value       = aws_dynamodb_table.order_idempotency_table.name
}
