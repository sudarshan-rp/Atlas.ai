aws_region         = "us-east-1"
environment        = "development"
project_name       = "document-api"
vpc_cidr           = "10.0.0.0/16"
cluster_name       = "document-api-cluster"
cluster_version    = "1.33"
node_instance_type = "t3.small"
node_desired_size  = 1
node_min_size      = 1
node_max_size      = 2

app_port    = 8008
api_version = "1.0.0"