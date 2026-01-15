# Lambda function
resource "aws_lambda_function" "lambda" {
  function_name = "lambda-powertools-metrics"
  role          = aws_iam_role.lambda_execution_role.arn
  image_uri     = "${aws_ecr_repository.lambda_repository.repository_url}:${local.docker_image_tag}"
  package_type  = "Image"
  architectures = ["arm64"]

  timeout     = 10
  memory_size = 128

  environment {
    variables = {
      POWERTOOLS_SERVICE_NAME      = "order-service"
      POWERTOOLS_METRICS_NAMESPACE = "order-service"
    }
  }

  depends_on = [null_resource.build_and_push_image]
}
