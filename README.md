# Document Processing API on AWS EKS

A containerized document processing API deployed on AWS EKS with complete CI/CD pipeline using GitHub Actions and Terraform.

## Architecture

### Components
- **VPC**: Custom VPC with public and private subnets across 2 availability zones
- **EKS Cluster**: Kubernetes 1.33 cluster for container orchestration
- **Node Group**: Auto-scaling t3.small EC2 instances (1-2 nodes)
- **Application Load Balancer**: Internet-facing ALB managed by AWS Load Balancer Controller
- **ECR**: Private Docker image registry
- **CloudWatch**: Centralized logging for application and cluster
- **IAM Roles**: IRSA (IAM Roles for Service Accounts) for secure AWS access

### Architecture Flow
```
Internet → ALB → EKS Cluster (Private Subnets) → Document API Pods → CloudWatch Logs
```

### Key Design Decisions

**Why EKS?**
- Industry-standard Kubernetes for container orchestration
- Better for microservices and future scalability
- Portable across cloud providers

**Why ALB over API Gateway?**
- Native integration with EKS via AWS Load Balancer Controller
- Lower latency for container workloads
- Cost-effective for sustained traffic

**Why Terraform?**
- Infrastructure as Code with state management
- Modular and reusable configurations
- Strong AWS provider support

**Why GitHub Actions?**
- Native CI/CD integration with GitHub
- OIDC authentication (no static credentials)
- Easy workflow management

## How to Deploy

### Prerequisites
1. AWS Account with appropriate permissions
2. GitHub repository
3. AWS CLI installed locally

### Step 1: Configure GitHub Secrets
Add the following secret to your GitHub repository (Settings → Secrets and variables → Actions):

- `AWS_IAM_ROLE`: ARN of the IAM role for GitHub Actions OIDC (e.g., `arn:aws:iam::ACCOUNT_ID:role/OIDC`)

### Step 2: Deploy Infrastructure
1. Go to **Actions** tab in GitHub
2. Select **Terraform Infrastructure** workflow
3. Click **Run workflow**
4. Choose action: `apply`
5. Wait for infrastructure to be created (~10-15 minutes)

### Step 3: Deploy Application
1. Push code to `main` branch or manually trigger **Build and Deploy** workflow
2. The workflow will:
   - Run tests
   - Build Docker image
   - Push to ECR
   - Deploy to EKS
   - Verify deployment

### Step 4: Access the API
Get the ALB endpoint:
```bash
kubectl get ingress document-api-ingress -n default
```

Test the API:
```bash
# Health check
curl http://<ALB-DNS>/health

# Upload document
curl -X POST -F "file=@test.txt" http://<ALB-DNS>/process
```

### Cleanup
1. Go to **Actions** tab
2. Select **Terraform Infrastructure** workflow
3. Click **Run workflow**
4. Choose action: `destroy`

## Challenges Faced

### 1. CloudWatch Addon Installation Failure
**Problem**: The CloudWatch observability addon failed during Terraform apply with error about ALB webhook not being available.

**Solution**: Added explicit dependency in Terraform to ensure ALB Controller is fully deployed before installing CloudWatch addon:
```hcl
depends_on = [
  aws_eks_node_group.main,
  helm_release.alb_controller
]
```

### 2. Deployment Timeout - Pod Scheduling
**Problem**: Rolling deployment failed with timeout because new pods couldn't be scheduled - "Too many pods" error on single t3.small node.

**Solution**: Changed deployment strategy from `RollingUpdate` to `Recreate` to avoid needing extra capacity during updates:
```yaml
spec:
  strategy:
    type: Recreate
```

### 3. ALB Not Deleted on Terraform Destroy
**Problem**: ALB created by Kubernetes Ingress wasn't deleted when running `terraform destroy`, causing destroy to fail.

**Solution**: Added pre-destroy step in workflow to delete Kubernetes ingress resources before Terraform destroy:
```bash
kubectl delete ingress --all -n default
```

### 4. Hardcoded AWS Account IDs
**Problem**: AWS account IDs were hardcoded in multiple files (k8s.yaml, aws-auth.yaml, terraform files), making the repo not shareable.

**Solution**: Replaced with `$AWS_ACCOUNT_ID` placeholder and used `envsubst` in GitHub Actions to substitute dynamically:
```bash
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
envsubst < k8s.yaml | kubectl apply -f -
```

### 5. GitHub Actions OIDC Authentication
**Problem**: Initial setup used static AWS credentials which is a security risk.

**Solution**: Implemented OIDC authentication with IAM role assumption, eliminating need for long-lived credentials in GitHub secrets.

## API Endpoints

- `GET /` - Welcome message
- `GET /health` - Health check
- `POST /process` - Upload and process document (multipart/form-data with `file` field)

## Technologies Used

- **Infrastructure**: Terraform, AWS EKS, VPC, ALB, ECR
- **Container**: Docker, Kubernetes
- **CI/CD**: GitHub Actions with OIDC
- **Application**: Python, FastAPI
- **Monitoring**: CloudWatch Logs
