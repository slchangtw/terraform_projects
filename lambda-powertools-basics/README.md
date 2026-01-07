# Lambda Powertools Basics

This example shows how to deploy a Lambda function  that uses AWS Lambda Powertools for Python to parse events and handle logging.

## Features

- Structured logging: JSON structured logging with `aws-lambda-powertools` logger utility.
- Validation: Input event validation using Pydantic models (`OrderDetails`).

## Deployment

```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply
```

## Remove the infrastructure

```bash
terraform -chdir=terraform destroy
```

