output "lambda_function_arn" {
  description = "The ARN of the Lambda function"
  value       = aws_lambda_function.lambda.arn
}

output "sqs_queue_url" {
  description = "The URL of the SQS queue"
  value       = aws_sqs_queue.main_queue.url
}

output "sqs_dlq_url" {
  description = "The URL of the Dead Letter Queue"
  value       = aws_sqs_queue.dlq.url
}
