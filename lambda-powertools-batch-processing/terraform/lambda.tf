# Lambda function
resource "aws_lambda_function" "lambda" {
  function_name = "lambda-powertools-batch-processing"
  role          = aws_iam_role.lambda_execution_role.arn
  image_uri     = "${aws_ecr_repository.lambda_repository.repository_url}:${local.docker_image_tag}"
  package_type  = "Image"
  architectures = ["arm64"]

  timeout     = 30
  memory_size = 128

  tracing_config {
    mode = "Active"
  }

  environment {
    variables = {
      POWERTOOLS_SERVICE_NAME = "batch-processing-service"
      POWERTOOLS_METRICS_NAMESPACE = "batch-processing-service"
    }
  }

  depends_on = [null_resource.build_and_push_image]
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
}

resource "aws_lambda_event_source_mapping" "sqs_trigger" {
  event_source_arn = aws_sqs_queue.main_queue.arn
  function_name    = aws_lambda_function.lambda.arn
  batch_size       = 10
  
  # Recommended for batch processing with partial failures
  function_response_types = ["ReportBatchItemFailures"]
}
