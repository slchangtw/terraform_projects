# AWS Service Answerer using AWS Bedrock

A Streamlit web application that provides expert answers about AWS services using Amazon Bedrock.

## Features
- The Terraform script creates a Lambda function that uses Amazon Bedrock to answer questions only related to AWS services and an API Gateway endpoint that invokes the Lambda function.
- Once the infrastructure is deployed, you can launch a Gradio web application, which reads the API Gateway URL from the Terraform outputs.

## Deployment via Terraform

```bash
terraform init
terraform -chdir=terraform apply
```

## Launch the web application 

```bash
uv run gradio run ui/gradio_app.py
```

## Remove the infrastructure

```bash
terraform -chdir=terraform destroy
```