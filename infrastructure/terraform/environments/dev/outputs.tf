output "aws_region" {
  description = "AWS region configured for this environment."
  value       = var.aws_region
}

output "vpc_id" {
  description = "Development VPC ID."
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "Public subnet IDs for the ALB."
  value       = aws_subnet.public[*].id
}

output "private_app_subnet_ids" {
  description = "Private application subnet IDs for ECS tasks."
  value       = aws_subnet.private_app[*].id
}

output "private_db_subnet_ids" {
  description = "Private database subnet IDs for RDS."
  value       = aws_subnet.private_db[*].id
}

output "api_ecr_repository_url" {
  description = "Backend/API ECR repository URL."
  value       = aws_ecr_repository.backend.repository_url
}

output "frontend_ecr_repository_url" {
  description = "Frontend ECR repository URL."
  value       = aws_ecr_repository.frontend.repository_url
}

output "ecs_cluster_name" {
  description = "ECS cluster name."
  value       = aws_ecs_cluster.main.name
}

output "ecs_cluster_arn" {
  description = "ECS cluster ARN."
  value       = aws_ecs_cluster.main.arn
}

output "alb_dns_name" {
  description = "Application Load Balancer DNS name."
  value       = aws_lb.app.dns_name
}

output "rds_endpoint" {
  description = "RDS PostgreSQL endpoint without credentials."
  value       = aws_db_instance.postgres.endpoint
}

output "database_secret_arn" {
  description = "Secrets Manager ARN containing the API DATABASE_URL."
  value       = aws_secretsmanager_secret.database_url.arn
}

output "api_target_group_arn" {
  description = "API target group ARN."
  value       = aws_lb_target_group.api.arn
}

output "frontend_target_group_arn" {
  description = "Frontend target group ARN."
  value       = aws_lb_target_group.frontend.arn
}

output "cloudwatch_log_group_names" {
  description = "CloudWatch log groups for ECS tasks."
  value = {
    api          = aws_cloudwatch_log_group.api.name
    frontend     = aws_cloudwatch_log_group.frontend.name
    backend_jobs = aws_cloudwatch_log_group.backend_jobs.name
  }
}
