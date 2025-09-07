locals {
  lambda_source_path = "../lambda"
}

# Package the Lambda function code
data "archive_file" "lambda_function_archive" {
  type        = "zip"
  source_file = "${local.lambda_source_path}/app.py"
  output_path = "${local.lambda_source_path}/function.zip"
}

resource "aws_lambda_permission" "apigw_lambda" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "arn:aws:execute-api:${data.aws_region.current.region}:${data.aws_caller_identity.current.account_id}:${aws_api_gateway_rest_api.api.id}/*/${aws_api_gateway_method.method_request.http_method}${aws_api_gateway_resource.resource.path}"
}

# Lambda function
resource "aws_lambda_function" "lambda" {
  filename         = data.archive_file.lambda_function_archive.output_path
  function_name    = "aws-service-advisor"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "app.lambda_handler"
  source_code_hash = data.archive_file.lambda_function_archive.output_base64sha256

  runtime = "python3.12"

  environment {
    variables = {
      MAX_INPUT_CHARACTERS = 1024
      MODEL_ID = "eu.amazon.nova-lite-v1:0"
    }
  }
}