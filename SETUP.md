# EKS Deployment Setup

## What's Automated

The Terraform configuration now automatically:
1. Creates EKS cluster with OIDC provider
2. Creates IAM roles for:
   - EKS cluster
   - Node groups
   - Application service account
   - AWS Load Balancer Controller
3. Installs AWS Load Balancer Controller via Helm
4. Configures all necessary IAM policies

## Initial Setup

### 1. Deploy Infrastructure

```bash
cd terraform
terraform init
terraform plan
terraform apply
```

### 2. Configure kubectl

```bash
aws eks update-kubeconfig --region us-east-1 --name document-api-cluster
```

### 3. Configure aws-auth for GitHub Actions

```bash
kubectl apply -f ../aws-auth.yaml
```

### 4. Deploy Application

```bash
kubectl apply -f ../k8s.yaml
kubectl apply -f ../ingress.yaml
```

Or push to GitHub and let Actions handle it.

## Verify Installation

```bash
# Check nodes
kubectl get nodes

# Check AWS LB Controller
kubectl get pods -n kube-system | grep aws-load-balancer

# Check ingress
kubectl get ingress -n default
```

## Troubleshooting

### ALB Controller not creating ALB
- Check controller logs: `kubectl logs -n kube-system deployment/aws-load-balancer-controller`
- Verify IAM role has policy attached
- Restart controller: `kubectl rollout restart deployment/aws-load-balancer-controller -n kube-system`

### GitHub Actions can't access cluster
- Verify OIDC role is in aws-auth ConfigMap
- Check role ARN matches in aws-auth.yaml

### Pods failing health checks
- Verify port numbers match in: Dockerfile, k8s.yaml (containerPort, service targetPort, probes)
