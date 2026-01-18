# Lambda Powertools Metrics

This example shows how to use AWS Lambda Powertools for Python to create custom CloudWatch Metrics and visualize them in a Dashboard.

## Features

- Custom Metrics: Uses `aws-lambda-powertools` Metrics utility to create business metrics (e.g., `SuccessfulOrders`).
- CloudWatch Metrics: Send metrics to CloudWatch with custom dimensions (e.g., item type) and metadata.
  <img src="../assets/lambda-powertools-metrics/dashboard_example.png" width="400" height="200" alt="Dashboard Example">

## Deployment

```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply
```

## Remove the infrastructure

```bash
terraform -chdir=terraform destroy
```
