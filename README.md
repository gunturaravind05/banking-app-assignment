# Banking Application Deployment on AWS using Terraform

## Project Overview

This project demonstrates an enterprise-style AWS deployment for a containerized banking application using Terraform and AWS native CI/CD services.

The solution is designed with:

- Infrastructure as Code (Terraform)
- Modular reusable architecture
- Secure networking
- CI/CD automation
- Containerized deployment
- Monitoring and alerting
- Secrets management
- High availability design

---

# Architecture

## AWS Services Used

- Amazon VPC
- Public and Private Subnets
- NAT Gateway
- Security Groups
- Application Load Balancer
- Amazon ECS Fargate
- Amazon ECR
- Amazon RDS MySQL
- AWS Secrets Manager
- Amazon CloudWatch
- Amazon SNS
- AWS CodeBuild
- AWS CodePipeline
- AWS CodeStar Connections
- Amazon S3
- Amazon DynamoDB

---

# CI/CD Flow

GitHub
  ↓
CodePipeline
  ↓
CodeBuild
  ↓
Amazon ECR
  ↓
Amazon ECS Fargate
  ↓
Application Load Balancer


## Features

Infrastructure
Modular Terraform structure
Reusable Terraform modules
Remote Terraform backend
State locking using DynamoDB
Multi-AZ deployment
Separate public/private subnets

## Security

ECS tasks in private subnets
RDS not publicly accessible
ALB is the only public entry point
Secrets stored in AWS Secrets Manager
Security group least privilege access
Encrypted Terraform state storage

## CI/CD
GitHub integrated pipeline
Automated Docker build
Automated ECR push
Automated ECS deployment
Linux AMD64 Docker builds for ECS compatibility

## Monitoring

CloudWatch Logs
CloudWatch Alarms
SNS alert notifications

## Repository Structure

banking-app-assignment/
├── app/
├── pipeline/
├── terraform/
│   ├── bootstrap/
│   ├── envs/
│   └── modules/
└── docs/

## Deployment Guide

Refer: docs/deployment-guide.md

## Architecture Diagram

Refer: docs/architecture.md & docs/architecture-diagram.png


## Future Security Improvements
HTTPS using ACM
AWS WAF
AWS GuardDuty
AWS Config
VPC Flow Logs
IAM least privilege refinement
Security scanning with tfsec/checkov