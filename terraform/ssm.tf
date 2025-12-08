resource "aws_ssm_parameter" "api_version" {
  name        = "/${var.project_name}/api_version"
  description = "API version"
  type        = "String"
  value       = var.api_version

  tags = {
    Name = "${var.project_name}-api-version"
  }
}

resource "aws_ssm_parameter" "environment" {
  name        = "/${var.project_name}/environment"
  description = "Environment name"
  type        = "String"
  value       = var.environment

  tags = {
    Name = "${var.project_name}-environment"
  }
}

resource "aws_ssm_parameter" "app_port" {
  name        = "/${var.project_name}/app_port"
  description = "Application port"
  type        = "String"
  value       = tostring(var.app_port)

  tags = {
    Name = "${var.project_name}-app-port"
  }
}

# Example secure parameter (for secrets)
resource "aws_ssm_parameter" "api_secret" {
  name        = "/${var.project_name}/api_secret"
  description = "API secret key"
  type        = "SecureString"
  value       = "change-me-in-production"

  tags = {
    Name = "${var.project_name}-api-secret"
  }

  lifecycle {
    ignore_changes = [value]
  }
}