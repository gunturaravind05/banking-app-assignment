# Deployment Guide

## 1. Prerequisites

Install the following tools:

- AWS CLI
- Terraform
- Docker
- Git

Configure AWS credentials:

```bash
aws configure

Verify access:
aws sts get-caller-identity

## 2. Repository Structure

banking-app-assignment/
├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       └── app.py
├── pipeline/
│   └── buildspec.yml
├── terraform/
│   ├── bootstrap/
│   ├── envs/
│   │   └── dev/
│   └── modules/
└── docs/

## 3. Bootstrap Terraform Backend
The bootstrap module creates:

S3 bucket for Terraform state
DynamoDB table for state locking

cd terraform/bootstrap
terraform init
terraform plan
terraform apply

## 4. Deploy Dev Environment

cd terraform/envs/dev
terraform init -backend-config=backend.hcl
terraform plan
terraform apply

This provisions:

VPC
Public and private subnets
NAT Gateway
Security groups
ALB
ECR
RDS MySQL
ECS Fargate
Secrets Manager
CloudWatch logs and alarms
SNS topic
CodeBuild
CodePipeline

## 5. GitHub Connection Authorization

After Terraform creates the CodeStar connection: AWS Console → CodePipeline → Settings → Connections

Authorize the GitHub connection for: gunturaravind05/banking-app-assignment

Connection status should become: AVAILABLE


## 6. CI/CD Deployment

Push code to GitHub:

git add .
git commit -m "Update application or infrastructure"
git push origin main

Pipeline flow: GitHub → CodePipeline → CodeBuild → ECR → ECS Fargate

## 7. Verify Application

Get ALB DNS: terraform output alb_dns_name

Test health endpoint: curl http://$(terraform output -raw alb_dns_name)/health

Expected response: {"status":"healthy"}

Test root endpoint: curl http://$(terraform output -raw alb_dns_name)/

Expected response: {"application":"banking-app","status":"running"}

## 8. Verify ECS Service
aws ecs describe-services \
  --cluster banking-app-dev-cluster \
  --services banking-app-dev-service \
  --region ap-southeast-1

  Expected:
  runningCount = 1
  desiredCount = 1

## 9. Verify Target Group Health

aws elbv2 describe-target-health \
  --target-group-arn $(terraform output -raw target_group_arn) \
  --region ap-southeast-1

  Expected: TargetHealth.State = healthy

## 10. Verify Monitoring
aws cloudwatch describe-alarms \
  --region ap-southeast-1 \
  --query 'MetricAlarms[*].AlarmName'

Expected alarms:
banking-app-dev-alb-5xx-high
banking-app-dev-unhealthy-targets
banking-app-dev-ecs-cpu-high
banking-app-dev-ecs-memory-high
banking-app-dev-rds-cpu-high

## 11. Verify Logs
Application logs are available in: CloudWatch Logs → /ecs/banking-app-dev

CodeBuild logs are available in: CloudWatch Logs → /codebuild/banking-app-dev

## 12. Destroy Environment
cd terraform/envs/dev
terraform destroy

## 13. Notes
ECS tasks run in private subnets.
RDS is not publicly accessible.
DB password is stored in AWS Secrets Manager.
Terraform state is stored in S3 with DynamoDB locking.
CI/CD builds Linux AMD64 images to support ECS Fargate.