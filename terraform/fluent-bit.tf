# Fluent Bit for CloudWatch Logs
resource "aws_eks_addon" "aws_for_fluent_bit" {
  cluster_name = aws_eks_cluster.main.name
  addon_name   = "aws-for-fluent-bit"

  depends_on = [aws_eks_node_group.main]
}
