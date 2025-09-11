# Hello World Lambda

This example demonstrates how to deploy two Lambda functions (dev and prod) with different environment variables.

## Architecture

<img src="../assets/hello-world-lambda/architecture.svg" alt="Architecture Diagram">

## Features

- The Terraform script creates two Lambda functions, one for the dev environment and one for the prod environment.
- In real-life scenarios, you can test the Lambda function using dev environment variables (such as an test email address instead of a real customer email address). Once the tests are done, you can promote the Lambda function to the prod environment.

## Deployment

```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply
```

## Remove the infrastructure
```bash
terraform -chdir=terraform destroy
```

