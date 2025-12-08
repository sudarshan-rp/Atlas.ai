# Automated AWS Load Balancer Controller Setup

## What Was Added

### 1. Terraform Files

**`terraform/alb-controller.tf`** - New file that:
- Downloads IAM policy from AWS GitHub (no local file needed)
- Creates IAM policy for AWS Load Balancer Controller
- Creates IAM role with IRSA for the controller
- Installs AWS Load Balancer Controller via Helm automatically

**`terraform/main.tf`** - Updated to include Helm and HTTP providers

### 2. How It Works

When you run `terraform apply`:
1. Creates EKS cluster with OIDC provider
2. Creates IAM role: `document-api-alb-controller-role`
3. Attaches AWS Load Balancer Controller IAM policy
4. Installs Helm chart for AWS Load Balancer Controller
5. Controller automatically creates ALB when you apply ingress.yaml

### 3. Next Deployment

For a fresh deployment:

```bash
# 1. Deploy infrastructure (includes ALB controller)
cd terraform
terraform apply

# 2. Configure kubectl
aws eks update-kubeconfig --region us-east-1 --name document-api-cluster

# 3. Add GitHub Actions access
kubectl apply -f ../aws-auth.yaml

# 4. Deploy app (or let GitHub Actions do it)
kubectl apply -f ../k8s.yaml
kubectl apply -f ../ingress.yaml
```

### 4. What's Automated vs Manual

**Automated (via Terraform):**
- ✅ EKS cluster creation
- ✅ IAM roles and policies
- ✅ AWS Load Balancer Controller installation
- ✅ VPC, subnets, security groups

**Manual (one-time per cluster):**
- ⚠️ aws-auth ConfigMap (for GitHub Actions access)
- ⚠️ Application deployment (or use GitHub Actions)

### 5. GitHub Actions Integration

The workflow already handles:
- Building and pushing Docker images
- Applying aws-auth ConfigMap
- Deploying k8s manifests
- Updating deployment with new images

## Benefits

- **No manual Helm installation needed**
- **ALB Controller ready on cluster creation**
- **Consistent across environments**
- **Infrastructure as Code**

## Cleanup

To destroy everything:
```bash
cd terraform
terraform destroy
```

This will:
- Delete ALB Controller
- Delete EKS cluster
- Delete all IAM roles
- Delete VPC and networking
