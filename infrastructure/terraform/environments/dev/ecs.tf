resource "aws_ecs_cluster" "main" {
  name = local.cluster_name

  setting {
    name  = "containerInsights"
    value = var.enable_ecs_container_insights ? "enabled" : "disabled"
  }

  tags = {
    Name = local.cluster_name
  }
}

resource "terraform_data" "ecs_image_validation" {
  count = var.create_ecs_services && !local.create_ecs_runtime ? 1 : 0

  lifecycle {
    precondition {
      condition     = !var.create_ecs_services || (var.api_image_uri != "" && var.frontend_image_uri != "")
      error_message = "create_ecs_services requires non-empty api_image_uri and frontend_image_uri values."
    }
  }
}

resource "aws_ecs_task_definition" "api" {
  count = local.create_ecs_runtime ? 1 : 0

  family                   = local.api_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.api_cpu
  memory                   = var.api_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.api_task.arn

  container_definitions = jsonencode([
    {
      name      = "api"
      image     = var.api_image_uri
      essential = true
      command   = ["api"]
      portMappings = [
        {
          containerPort = var.api_container_port
          hostPort      = var.api_container_port
          protocol      = "tcp"
        }
      ]
      environment = [
        { name = "APP_ENV", value = "production" },
        { name = "API_PORT", value = tostring(var.api_container_port) },
        { name = "RUN_MIGRATIONS_ON_STARTUP", value = "false" },
        { name = "SYNC_OUTPUTS_ON_STARTUP", value = "false" },
        { name = "LLM_ENABLED", value = "false" },
        { name = "AGENT_MODE", value = "deterministic" },
        { name = "LLM_FALLBACK_ENABLED", value = "true" },
        { name = "OPENAI_MODEL", value = "" }
      ]
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret.database_url.arn
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.api.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "api"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "frontend" {
  count = local.create_ecs_runtime ? 1 : 0

  family                   = local.frontend_name
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.frontend_cpu
  memory                   = var.frontend_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.frontend_task.arn

  container_definitions = jsonencode([
    {
      name      = "frontend"
      image     = var.frontend_image_uri
      essential = true
      portMappings = [
        {
          containerPort = var.frontend_container_port
          hostPort      = var.frontend_container_port
          protocol      = "tcp"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.frontend.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "frontend"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "migration" {
  count = local.create_ecs_runtime ? 1 : 0

  family                   = "${local.name_prefix}-migration"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.api_cpu
  memory                   = var.api_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.api_task.arn

  container_definitions = jsonencode([
    {
      name      = "migration"
      image     = var.api_image_uri
      essential = true
      command   = ["migrate"]
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret.database_url.arn
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.backend_jobs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "migration"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "sync" {
  count = local.create_ecs_runtime ? 1 : 0

  family                   = "${local.name_prefix}-sync"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = var.api_cpu
  memory                   = var.api_memory
  execution_role_arn       = aws_iam_role.ecs_task_execution.arn
  task_role_arn            = aws_iam_role.api_task.arn

  container_definitions = jsonencode([
    {
      name      = "sync"
      image     = var.api_image_uri
      essential = true
      command   = ["sync"]
      secrets = [
        {
          name      = "DATABASE_URL"
          valueFrom = aws_secretsmanager_secret.database_url.arn
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.backend_jobs.name
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "sync"
        }
      }
    }
  ])
}

resource "aws_ecs_service" "api" {
  count = local.create_ecs_runtime ? 1 : 0

  name            = local.api_name
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.api[0].arn
  desired_count   = var.desired_api_task_count
  launch_type     = "FARGATE"

  health_check_grace_period_seconds = 60

  network_configuration {
    subnets          = aws_subnet.private_app[*].id
    security_groups  = [aws_security_group.api.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = var.api_container_port
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  depends_on = [
    aws_lb_listener.http,
    aws_lb_listener_rule.api,
    aws_iam_role_policy_attachment.ecs_task_execution_managed,
    aws_iam_role_policy.ecs_task_execution_secrets,
  ]
}

resource "aws_ecs_service" "frontend" {
  count = local.create_ecs_runtime ? 1 : 0

  name            = local.frontend_name
  cluster         = aws_ecs_cluster.main.id
  task_definition = aws_ecs_task_definition.frontend[0].arn
  desired_count   = var.desired_frontend_task_count
  launch_type     = "FARGATE"

  health_check_grace_period_seconds = 30

  network_configuration {
    subnets          = aws_subnet.private_app[*].id
    security_groups  = [aws_security_group.frontend.id]
    assign_public_ip = false
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.frontend.arn
    container_name   = "frontend"
    container_port   = var.frontend_container_port
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = true
  }

  depends_on = [
    aws_lb_listener.http,
    aws_iam_role_policy_attachment.ecs_task_execution_managed,
  ]
}
