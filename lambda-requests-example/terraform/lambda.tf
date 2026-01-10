# Lambda function
resource "aws_lambda_function" "lambda" {
  function_name = "lambda-requests-example"
  role          = aws_iam_role.lambda_execution_role.arn
  image_uri     = "${aws_ecr_repository.lambda_repository.repository_url}:latest"
  package_type  = "Image"
  architectures = ["arm64"]

  source_code_hash = null_resource.build_and_push_image.triggers.lambda_code_hash

  timeout = 10

  depends_on = [null_resource.build_and_push_image]
}
