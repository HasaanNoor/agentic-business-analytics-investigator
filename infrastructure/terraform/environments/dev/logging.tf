resource "aws_cloudwatch_log_group" "api" {
  name              = local.api_log_group_name
  retention_in_days = var.log_retention_days

  tags = {
    Name = local.api_log_group_name
  }
}

resource "aws_cloudwatch_log_group" "frontend" {
  name              = local.frontend_log_group_name
  retention_in_days = var.log_retention_days

  tags = {
    Name = local.frontend_log_group_name
  }
}

resource "aws_cloudwatch_log_group" "backend_jobs" {
  name              = local.backend_job_log_group_name
  retention_in_days = var.log_retention_days

  tags = {
    Name = local.backend_job_log_group_name
  }
}
