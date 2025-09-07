terraform {
  required_version = "~> 1.13"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
  # Please update the bucket name to the one created by the bootstrap project
  backend "s3" {
    bucket = "terraform-state-bucket-3517e72f-9d72-c38f-b9c6-6a025a99c78b"
    key    = "vpc-ec2-nginx/terraform.tfstate"
    region = "eu-central-1"
  }
}

provider "aws" {
  region = "eu-central-1"
  default_tags {
    tags = {
      ManagedBy = "Terraform"
      Project   = "nginx-server"
    }
  }
}
