# Amazon CloudWatch Observability addon for container logs
resource "aws_eks_addon" "cloudwatch_observability" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "amazon-cloudwatch-observability"

  depends_on = [
    aws_eks_node_group.main,
    helm_release.alb_controller
  ]
}
