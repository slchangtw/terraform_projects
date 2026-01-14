resource "aws_lambda_function" "lambda" {
  function_name = "lambda-requests-example"
  role          = aws_iam_role.lambda_execution_role.arn
  image_uri     = "${aws_ecr_repository.lambda_repository.repository_url}:${local.docker_image_tag}"
  package_type  = "Image"
  architectures = ["arm64"]

  timeout = 10
  memory_size = 128

  depends_on = [null_resource.build_and_push_image]
}
