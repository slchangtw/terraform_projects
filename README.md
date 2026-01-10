# Terraform Projects

This repository contains various Terraform projects for provisioning AWS services.

## Prerequisites

- Terraform
- AWS CLI with credentials configured
- `uv` as Python package manager, you can install the dependencies using `uv sync --all-groups`
- Run [bootstrap](boostrap): bootstrap the infrastructure for other projects.

## Projects

- [hello-world-lambda](hello-world-lambda): A simple Lambda function that returns "Hello World" with a custom message based on the environment variable.
- [lambda-apigateway](lambda-apigateway): An example of how to deploy a Lambda function and expose it via API Gateway.
- [vpc-ec2-nginx](vpc-ec2-nginx): An example of how to configure an EC2 instance running Nginx in a VPC.
- [bedrock-lambda](bedrock-lambda): A Lambda function that uses AWS Bedrock to answer questions about AWS services, with a Streamlit UI for interaction.

### AWS Lambda Powertools

These projects demonstrate how to enhance Lambda functions using AWS Lambda Powertools for Python.

- [lambda-powertools-basics](lambda-powertools-basics): Event parsing and structured JSON logging.
- [lambda-powertools-metrics](lambda-powertools-metrics): Custom metrics tracking.
- [lambda-powertools-tracer](lambda-powertools-tracer): Execution tracing with AWS X-Ray.
- [lambda-powertools-idempotency](lambda-powertools-idempotency): Idempotent execution handling.
