locals {
  name_prefix = "${var.project_code}-${var.environment}"

  common_tags = merge(
    {
      Project     = var.project_name
      ProjectCode = var.project_code
      Environment = var.environment
      ManagedBy   = "Terraform"
    },
    var.additional_tags,
  )

  vpc_name                   = "${local.name_prefix}-vpc"
  api_name                   = "${local.name_prefix}-api"
  frontend_name              = "${local.name_prefix}-frontend"
  db_name                    = "${local.name_prefix}-db"
  cluster_name               = "${local.name_prefix}-cluster"
  alb_name                   = "${local.name_prefix}-alb"
  backend_ecr_name           = "${local.name_prefix}-backend"
  frontend_ecr_name          = "${local.name_prefix}-frontend"
  database_secret_name       = "${local.name_prefix}/database-url"
  api_log_group_name         = "/ecs/${local.name_prefix}/api"
  frontend_log_group_name    = "/ecs/${local.name_prefix}/frontend"
  backend_job_log_group_name = "/ecs/${local.name_prefix}/backend-jobs"

  subnet_count = min(
    length(var.availability_zones),
    length(var.public_subnet_cidrs),
    length(var.private_app_subnet_cidrs),
    length(var.private_db_subnet_cidrs),
  )

  availability_zones       = slice(var.availability_zones, 0, local.subnet_count)
  public_subnet_cidrs      = slice(var.public_subnet_cidrs, 0, local.subnet_count)
  private_app_subnet_cidrs = slice(var.private_app_subnet_cidrs, 0, local.subnet_count)
  private_db_subnet_cidrs  = slice(var.private_db_subnet_cidrs, 0, local.subnet_count)

  create_ecs_runtime = var.create_ecs_services && var.api_image_uri != "" && var.frontend_image_uri != ""

  database_url = "postgresql+psycopg2://${var.database_username}:${random_password.database_password.result}@${aws_db_instance.postgres.address}:5432/${var.database_name}"
}
