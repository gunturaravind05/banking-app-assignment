# Banking Application AWS Architecture

## Overview

This project deploys a secure and scalable banking REST API on AWS using Terraform and AWS native CI/CD services.

## Architecture Flow

GitHub
  ↓
AWS CodePipeline
  ↓
AWS CodeBuild
  ↓
Amazon ECR
  ↓
Amazon ECS Fargate
  ↓
Application Load Balancer
  ↓
Amazon RDS MySQL


## AWS Components
VPC with public and private subnets
Application Load Balancer in public subnets
ECS Fargate service in private app subnets
RDS MySQL in private DB subnets
ECR for Docker image storage
Secrets Manager for database password
CloudWatch Logs for ECS application logs
CloudWatch Alarms for ALB, ECS, and RDS monitoring
SNS topic for alert notifications
CodePipeline and CodeBuild for CI/CD

## Security Design
RDS is not publicly accessible
ECS tasks run in private subnets
ALB is the only public entry point
ALB allows HTTP traffic from internet
ECS security group allows traffic only from ALB
RDS security group allows MySQL only from ECS
DB password is stored in AWS Secrets Manager
Terraform state is stored in encrypted S3 with DynamoDB locking

## CI/CD Flow
Developer pushes code to GitHub
CodePipeline detects the change
CodeBuild builds a Linux AMD64 Docker image
Image is pushed to Amazon ECR
ECS service is force redeployed
ALB routes traffic to the new healthy ECS task

## Monitoring
CloudWatch alarms are configured for:
ALB 5XX errors
ALB unhealthy targets
ECS CPU utilization
ECS memory utilization
RDS CPU utilization