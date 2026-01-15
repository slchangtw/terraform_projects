# Get ECR login token
data "aws_ecr_authorization_token" "token" {}

locals {
  # Calculate a hash of all source files to use as the image tag
  docker_image_tag = md5(join("", [
    filemd5("../Dockerfile"),
    filemd5("../pyproject.toml"),
    join("", [for f in fileset("../lambda", "**") : filemd5("../lambda/${f}")])
  ]))
}

resource "aws_ecr_repository" "lambda_repository" {
  name         = "lambda-powertools-basics"
  force_delete = true
}

# Build and push Docker image
resource "null_resource" "build_and_push_image" {
  triggers = {
    # Trigger rebuild when the image tag changes (which means source files changed)
    image_tag = local.docker_image_tag
  }

  provisioner "local-exec" {
    command = <<-EOT
      # Login to ECR
      echo ${data.aws_ecr_authorization_token.token.password} | docker login --username AWS --password-stdin ${data.aws_ecr_authorization_token.token.proxy_endpoint}
      
      # Build the image
      docker build --platform linux/arm64 -t ${aws_ecr_repository.lambda_repository.repository_url}:${local.docker_image_tag} ..
      
      # Push the image
      docker push ${aws_ecr_repository.lambda_repository.repository_url}:${local.docker_image_tag}
    EOT
  }

  depends_on = [aws_ecr_repository.lambda_repository]
}
