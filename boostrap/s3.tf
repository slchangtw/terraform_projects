resource "random_uuid" "bucket_name" {}

resource "aws_s3_bucket" "terraform_state" {
  bucket = "terraform-state-bucket-${random_uuid.bucket_name.id}"

  tags = {
    Name        = "Terraform State Bucket"
    Environment = "Bootstrap"
  }
}