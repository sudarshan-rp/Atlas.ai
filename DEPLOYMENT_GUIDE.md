# Complete Deployment Guide

## Overview

This project has two GitHub Actions workflows:
1. **Terraform Infrastructure** - Deploys EKS cluster and AWS Load Balancer Controller
2. **Build and Deploy** - Builds Docker image and deploys application

## First Time Setup

### 1. Deploy Infrastructure via GitHub Actions

1. Go to GitHub Actions tab
2. Select "Terraform Infrastructure" workflow
3. Click "Run workflow"
4. Select action: **apply**
5. Wait for completion (~15 minutes)

This will:
- ✅ Create EKS cluster
- ✅ Create VPC, subnets, security groups
- ✅ Create IAM roles and policies
- ✅ Install AWS Load Balancer Controller
- ✅ Configure aws-auth for GitHub Actions access

### 2. Deploy Application

**Option A: Via GitHub Actions (Recommended)**
- Push to `main` branch
- Workflow automatically builds and deploys

**Option B: Manual**
```bash
aws eks update-kubeconfig --name document-api-cluster --region us-east-1
kubectl apply -f k8s.yaml
kubectl apply -f ingress.yaml
```

### 3. Get Application URL

```bash
kubectl get ingress document-api-ingress -n default
```

Or check the GitHub Actions output for the ALB endpoint.

## Subsequent Deployments

Just push to `main` branch - everything is automated!

```bash
git add .
git commit -m "Update application"
git push
```

The workflow will:
1. Run tests
2. Build Docker image
3. Push to ECR
4. Deploy to EKS
5. Update deployment with new image
6. Wait for rollout
7. Display ALB endpoint

## Workflows Explained

### Terraform Infrastructure Workflow

**Trigger:** Manual (workflow_dispatch)

**Actions:**
- `plan` - Show what will be created/changed
- `apply` - Deploy infrastructure
- `destroy` - Delete everything

**When to use:**
- Initial setup
- Infrastructure changes
- Cleanup

### Build and Deploy Workflow

**Trigger:** Automatic on push to `main`

**Steps:**
1. Run tests
2. Build Docker image for AMD64
3. Push to ECR
4. Configure kubectl
5. Verify ALB Controller
6. Apply k8s manifests
7. Update deployment image
8. Wait for rollout
9. Test endpoints

## Monitoring

### Check Deployment Status
```bash
kubectl get pods -n default
kubectl get deployments -n default
kubectl get ingress -n default
```

### Check Logs
```bash
kubectl logs -f deployment/document-api -n default
```

### Check ALB Controller
```bash
kubectl logs -n kube-system deployment/aws-load-balancer-controller
```

## Troubleshooting

### Deployment fails with "deployment not found"
- First deployment? Workflow handles this automatically
- Check if k8s.yaml was applied

### No ALB address in ingress
- Wait 2-3 minutes for ALB creation
- Check ALB Controller: `kubectl get pods -n kube-system | grep aws-load-balancer`
- Check controller logs for errors

### Pods in CrashLoopBackOff
- Check logs: `kubectl logs <pod-name>`
- Common issues:
  - Port mismatch (app vs k8s config)
  - Wrong CPU architecture (rebuild with --platform linux/amd64)
  - Health check failures

### GitHub Actions can't access cluster
- Verify aws-auth ConfigMap: `kubectl get cm aws-auth -n kube-system -o yaml`
- OIDC role should be present

## Cleanup

### Delete Application Only
```bash
kubectl delete -f ingress.yaml
kubectl delete -f k8s.yaml
```

### Delete Everything (Infrastructure + Application)
1. Go to GitHub Actions
2. Run "Terraform Infrastructure" workflow
3. Select action: **destroy**

Or locally:
```bash
cd terraform
terraform destroy
```

## Cost Optimization

- EKS cluster: ~$73/month
- Node groups (SPOT): ~$15-30/month
- ALB: ~$16/month
- Data transfer: Variable

**Total: ~$100-120/month**

To reduce costs:
- Use smaller instance types
- Reduce node count
- Use Fargate instead of node groups
