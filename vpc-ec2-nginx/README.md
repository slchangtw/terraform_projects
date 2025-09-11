# EC2 Nginx in a VPC

This project was adapted from [https://github.com/lm-academy/terraform-course/tree/main/06-resources](https://github.com/lm-academy/terraform-course/tree/main/06-resources). The scripts create an EC2 instance running Nginx in a VPC with networking and security groups configured.

## Deployment via Terraform

```bash
terraform init
terraform -chdir=terraform apply
```

## Remove the infrastructure

```bash
terraform -chdir=terraform destroy
```