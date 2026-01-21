resource "aws_lambda_function" "lambda" {
  function_name = "lambda-powertools-idempotency"
  role          = aws_iam_role.lambda_execution_role.arn
  image_uri     = "${aws_ecr_repository.lambda_repository.repository_url}:${local.docker_image_tag}"
  package_type  = "Image"
  architectures = ["arm64"]

  timeout     = 10
  memory_size = 128

  tracing_config {
    mode = "Active"
  }

  environment {
    variables = {
      POWERTOOLS_SERVICE_NAME      = "order-service"
      POWERTOOLS_METRICS_NAMESPACE = "order-service"
      IDEMPOTENCY_TABLE_NAME       = aws_dynamodb_table.order_idempotency_table.name
    }
  }

  depends_on = [null_resource.build_and_push_image]
}

resource "aws_cloudwatch_log_group" "lambda_log_group" {
  name              = "/aws/lambda/${aws_lambda_function.lambda.function_name}"
}
