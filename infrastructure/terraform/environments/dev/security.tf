resource "aws_security_group" "alb" {
  name        = "${local.name_prefix}-alb-sg"
  description = "Allow public HTTP traffic to the application load balancer"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTP from the internet"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description = "Forward traffic to private ECS tasks"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.vpc_cidr]
  }

  tags = {
    Name = "${local.name_prefix}-alb-sg"
  }
}

resource "aws_security_group" "api" {
  name        = "${local.name_prefix}-api-sg"
  description = "Allow API traffic only from the ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "API container port from ALB"
    from_port       = var.api_container_port
    to_port         = var.api_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "Outbound HTTPS and database traffic"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.name_prefix}-api-sg"
  }
}

resource "aws_security_group" "frontend" {
  name        = "${local.name_prefix}-frontend-sg"
  description = "Allow frontend traffic only from the ALB"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Frontend container port from ALB"
    from_port       = var.frontend_container_port
    to_port         = var.frontend_container_port
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description = "Outbound traffic for image and package runtime needs"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "${local.name_prefix}-frontend-sg"
  }
}

resource "aws_security_group" "database" {
  name        = "${local.name_prefix}-db-sg"
  description = "Allow PostgreSQL only from API ECS tasks"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "PostgreSQL from API tasks"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.api.id]
  }

  egress {
    description = "Database responses inside the VPC"
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [var.vpc_cidr]
  }

  tags = {
    Name = "${local.name_prefix}-db-sg"
  }
}
