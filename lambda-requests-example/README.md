# Lambda Requests Example

This project demonstrates how to containerize a Python Lambda function using `uv` and deploy it with Terraform. The function uses the `requests` library to fetch data from the GitHub API.


## Deployment

```bash
terraform -chdir=terraform init
terraform -chdir=terraform apply
```

## Remove the infrastructure

```bash
terraform -chdir=terraform destroy
```
