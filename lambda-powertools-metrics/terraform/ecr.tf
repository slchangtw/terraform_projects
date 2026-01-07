# Get ECR login token
data "aws_ecr_authorization_token" "token" {}

resource "aws_ecr_repository" "lambda_repository" {
  name         = "lambda-powertools-metrics"
  force_delete = true
}

# Build and push Docker image
resource "null_resource" "build_and_push_image" {
  triggers = {
    # Trigger rebuild when these files change
    dockerfile_hash  = filemd5("../Dockerfile")
    pyproject_hash   = filemd5("../pyproject.toml")
    lambda_code_hash = join(",", [for f in fileset("../lambda", "**") : filemd5("../lambda/${f}")])
  }

  provisioner "local-exec" {
    command = <<-EOT
      # Login to ECR
      echo ${data.aws_ecr_authorization_token.token.password} | docker login --username AWS --password-stdin ${data.aws_ecr_authorization_token.token.proxy_endpoint}
      
      # Build the image
      docker build --platform linux/arm64 -t ${aws_ecr_repository.lambda_repository.repository_url}:latest ..
      
      # Push the image
      docker push ${aws_ecr_repository.lambda_repository.repository_url}:latest
    EOT
  }

  depends_on = [aws_ecr_repository.lambda_repository]
}

