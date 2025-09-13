
resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"


  source_arn = "arn:aws:execute-api:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method_request.http_method}${aws_api_gateway_resource.resource.path}"
}

# Lambda function
resource "aws_lambda_function" "lambda" {
  function_name = "aws-service-advisor"
  role          = aws_iam_role.lambda_execution_role.arn
  image_uri     = "${aws_ecr_repository.lambda_repository.repository_url}:bedrock-lambda"
  package_type  = "Image"
  architectures = ["arm64"]

  timeout = 15

  environment {
    variables = {
      MAX_INPUT_CHARACTERS = 1024
      MODEL_ID             = "eu.amazon.nova-lite-v1:0"
    }
  }

  depends_on = [null_resource.build_and_push_image]
}