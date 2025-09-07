# Data sources for AWS account and region information
data "aws_caller_identity" "current" {}

data "aws_region" "current" {}
