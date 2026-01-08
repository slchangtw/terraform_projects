# Lambda function
resource "aws_lambda_function" "lambda" {
  function_name = "lambda-powertools-tracer"
  role          = aws_iam_role.lambda_execution_role.arn
  image_uri     = "${aws_ecr_repository.lambda_repository.repository_url}:latest"
  package_type  = "Image"
  architectures = ["arm64"]

  source_code_hash = null_resource.build_and_push_image.triggers.lambda_code_hash

  timeout = 10

  tracing_config {
    mode = "Active"
  }

  environment {   
    variables = {
      POWERTOOLS_SERVICE_NAME      = "order-service"
      POWERTOOLS_METRICS_NAMESPACE = "order-service"
    }
  }

  depends_on = [null_resource.build_and_push_image]
}
