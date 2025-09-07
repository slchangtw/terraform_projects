locals {
  lambda_source_path = "../lambda"
  environments = {
    dev = {
      memory_size = 128
      timeout     = 3
    }
    prod = {
      memory_size = 256
      timeout     = 10
    }
  }
}

variable "environment" {
  description = "Environment name (dev or prod)"
  type        = string
  default     = "dev"

  validation {
    condition     = contains(["dev", "prod"], var.environment)
    error_message = "Environment must be either 'dev' or 'prod'."
  }
}

# Package the Lambda function code
data "archive_file" "lambda_function_archive" {
  type        = "zip"
  source_file = "${local.lambda_source_path}/app.py"
  output_path = "${local.lambda_source_path}/function.zip"
}

# Lambda function
resource "aws_lambda_function" "lambda_function" {
  for_each = local.environments

  filename         = data.archive_file.lambda_function_archive.output_path
  function_name    = "hello-world-${each.key}"
  role             = aws_iam_role.lambda_execution_role.arn
  handler          = "app.handler"
  source_code_hash = data.archive_file.lambda_function_archive.output_base64sha256

  runtime     = "python3.12"
  memory_size = each.value.memory_size
  timeout     = each.value.timeout

  environment {
    variables = {
      ENVIRONMENT = each.key
    }
  }

  tags = {
    Environment = each.key 
  }
}
