aws_region         = "us-east-1"
environment        = "production"
project_name       = "document-api"
vpc_cidr           = "10.0.0.0/16"
cluster_name       = "document-api-cluster"
cluster_version    = "1.34"
node_instance_type = "t3.small"
node_desired_size  = 1
node_min_size      = 1
node_max_size      = 2

# Update this with your actual ECR image URL after pushing the image
docker_image = "771826808000.dkr.ecr.us-east-1.amazonaws.com/document-api:latest"

app_port    = 8008
api_version = "1.0.0"