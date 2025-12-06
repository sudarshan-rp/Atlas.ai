Document Processing API on AWS EKS
A containerized document processing API deployed on AWS EKS with complete CI/CD pipeline, infrastructure as code, and production-ready features.
📋 Table of Contents

Architecture
Features
Prerequisites
Quick Start
Deployment Guide
API Documentation
CI/CD Pipeline
Monitoring & Logs
Cost Estimation
Troubleshooting
Cleanup

🏗️ Architecture
High-Level Architecture
Internet
    ↓
Application Load Balancer (Public)
    ↓
EKS Cluster (Private Subnets)
    ↓
Document API Pods
    ↓
CloudWatch Logs
SSM Parameter Store
Components

VPC: Custom VPC with public and private subnets across 2 AZs
EKS Cluster: Kubernetes 1.28 cluster for container orchestration
Node Group: Auto-scaling group of t3.small EC2 instances
ALB: Internet-facing Application Load Balancer
ECR: Private Docker image registry
CloudWatch: Centralized logging and monitoring
SSM Parameter Store: Configuration management
IAM Roles: Service accounts with IRSA (IAM Roles for Service Accounts)

Design Decisions
Why EKS over ECS/Fargate?

Better for microservices architecture and future scalability
Kubernetes-native tooling and portability
More control over scheduling and resource management
Industry standard for container orchestration

Why ALB over API Gateway?

Better integration with EKS
Lower latency for container-to-container communication
More cost-effective for sustained traffic
Built-in health checks and auto-scaling

Why Terraform?

Declarative infrastructure as code
State management for tracking resources
Modular and reusable configurations
Strong AWS provider support

✨ Features

✅ RESTful API with file upload endpoint
✅ Containerized application with Docker
✅ Kubernetes deployment with auto-scaling
✅ Infrastructure as Code with Terraform
✅ CI/CD pipeline with GitHub Actions
✅ Centralized logging to CloudWatch
✅ Configuration management with SSM
✅ IAM roles with least privilege
✅ Health checks and readiness probes
✅ Public endpoint via ALB