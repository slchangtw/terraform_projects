# ECS Cluster with Fargate

This project creates an Amazon ECS cluster using AWS Fargate with a sample Nginx application. The infrastructure includes VPC networking, security groups, IAM roles, and an Application Load Balancer.

## Architecture

The infrastructure includes:
- **VPC** with public and private subnets across two availability zones
- **ECS Cluster** with Fargate launch type
- **ECS Service** running Nginx containers
- **Application Load Balancer** for traffic distribution
- **Security Groups** for network access control
- **IAM Roles** for ECS task execution and service management
- **CloudWatch Logs** for container logging


## Deployment via Terraform

1. Navigate to the terraform directory:
```bash
cd terraform
```

2. Initialize Terraform:
```bash
terraform init
```

3. Review the planned changes:
```bash
terraform plan
```

4. Apply the configuration:
```bash
terraform apply
```

5. When prompted, type `yes` to confirm the deployment.

## Accessing the Application

After deployment, you can access the Nginx application using the ALB DNS name from the Terraform outputs:

```bash
# Get the ALB DNS name
terraform output alb_dns_name
```

The application will be available at `http://<alb-dns-name>`.

## Monitoring

- **CloudWatch Logs**: Container logs are available in the `/ecs/ecs-cluster` log group
- **ECS Console**: Monitor service health and task status in the AWS ECS console
- **Load Balancer**: Check target health in the EC2 Load Balancer console

## Configuration Details

### Networking
- VPC CIDR: `10.0.0.0/16`
- Public subnets: `10.0.1.0/24` and `10.0.2.0/24`
- Private subnets: `10.0.3.0/24` and `10.0.4.0/24`
- NAT Gateway for private subnet internet access

### ECS Configuration
- Launch type: Fargate
- CPU: 256 units (0.25 vCPU)
- Memory: 512 MB
- Desired count: 2 tasks
- Container: Nginx latest

### Security
- Security groups restrict access to ports 80 and 443
- IAM roles follow least privilege principle
- Tasks run in public subnets with public IP assignment

## Customization

To customize the deployment:

1. **Change the container image**: Modify the `image` field in `ecs.tf`
2. **Adjust resources**: Update `cpu` and `memory` values in the task definition
3. **Modify scaling**: Change `desired_count` in the ECS service
4. **Update networking**: Modify CIDR blocks in `networking.tf`

## Remove the Infrastructure

To destroy all resources:

```bash
terraform destroy
```

When prompted, type `yes` to confirm the destruction.

**Warning**: This will permanently delete all resources created by this Terraform configuration.

## Troubleshooting

### Common Issues

1. **Service fails to start**: Check CloudWatch logs for container errors
2. **Tasks not registering with ALB**: Verify security group rules allow traffic on port 80
3. **DNS resolution issues**: Ensure the ALB is in public subnets with internet gateway access

### Useful Commands

```bash
# Check ECS service status
aws ecs describe-services --cluster ecs-cluster --services ecs-app-service-alb

# View task logs
aws logs tail /ecs/ecs-cluster --follow

# Check ALB target health
aws elbv2 describe-target-health --target-group-arn <target-group-arn>
```

