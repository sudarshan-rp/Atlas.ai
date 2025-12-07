# CloudWatch Log Group for EKS Cluster
resource "aws_cloudwatch_log_group" "eks_cluster" {
  name              = "/aws/eks/${var.cluster_name}/cluster"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-eks-cluster-logs"
  }
}

# CloudWatch Log Group for Application
resource "aws_cloudwatch_log_group" "application" {
  name              = "/aws/eks/${var.cluster_name}/application"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-application-logs"
  }
}

# CloudWatch Log Group for ALB
resource "aws_cloudwatch_log_group" "alb" {
  name              = "/aws/elasticloadbalancing/${var.project_name}"
  retention_in_days = 7

  tags = {
    Name = "${var.project_name}-alb-logs"
  }
}