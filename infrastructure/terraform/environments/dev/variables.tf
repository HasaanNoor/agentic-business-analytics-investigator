variable "aws_region" {
  description = "AWS region for the development environment."
  type        = string
  default     = "us-east-1"

  validation {
    condition     = length(trimspace(var.aws_region)) > 0
    error_message = "aws_region must not be blank."
  }
}

variable "project_name" {
  description = "Human-readable project name used in common tags."
  type        = string
  default     = "Agentic Business Analytics Investigator"
}

variable "project_code" {
  description = "Short project code used in resource names."
  type        = string
  default     = "abai"

  validation {
    condition     = can(regex("^[a-z][a-z0-9-]{1,15}$", var.project_code))
    error_message = "project_code must be lowercase, start with a letter, and contain only lowercase letters, numbers, and hyphens."
  }
}

variable "environment" {
  description = "Deployment environment name."
  type        = string
  default     = "dev"

  validation {
    condition     = length(trimspace(var.environment)) > 0
    error_message = "environment must not be blank."
  }
}

variable "additional_tags" {
  description = "Additional tags merged with the default project tags."
  type        = map(string)
  default     = {}
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC."
  type        = string
  default     = "10.20.0.0/16"
}

variable "availability_zones" {
  description = "Availability zones used for public, application, and database subnet tiers."
  type        = list(string)
  default     = ["us-east-1a", "us-east-1b"]

  validation {
    condition     = length(var.availability_zones) >= 2
    error_message = "At least two availability zones are required."
  }
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for public subnets that host the Application Load Balancer."
  type        = list(string)
  default     = ["10.20.0.0/24", "10.20.1.0/24"]

  validation {
    condition     = length(var.public_subnet_cidrs) >= 2
    error_message = "At least two public subnet CIDRs are required."
  }
}

variable "private_app_subnet_cidrs" {
  description = "CIDR blocks for private application subnets that host ECS tasks."
  type        = list(string)
  default     = ["10.20.10.0/24", "10.20.11.0/24"]

  validation {
    condition     = length(var.private_app_subnet_cidrs) >= 2
    error_message = "At least two private application subnet CIDRs are required."
  }
}

variable "private_db_subnet_cidrs" {
  description = "CIDR blocks for private database subnets that host RDS."
  type        = list(string)
  default     = ["10.20.20.0/24", "10.20.21.0/24"]

  validation {
    condition     = length(var.private_db_subnet_cidrs) >= 2
    error_message = "At least two private database subnet CIDRs are required."
  }
}

variable "enable_nat_gateway" {
  description = "Create one NAT gateway for private application subnet egress. This is cheaper than one per AZ but not AZ redundant."
  type        = bool
  default     = true
}

variable "database_name" {
  description = "Initial PostgreSQL database name."
  type        = string
  default     = "analytics_dev"

  validation {
    condition     = can(regex("^[A-Za-z][A-Za-z0-9_]{0,62}$", var.database_name))
    error_message = "database_name must start with a letter and contain only letters, numbers, and underscores."
  }
}

variable "database_username" {
  description = "PostgreSQL master username. Do not use the local development username."
  type        = string
  default     = "abai_admin"

  validation {
    condition     = !contains(["analytics_user"], var.database_username)
    error_message = "database_username must not use the local development username."
  }
}

variable "database_instance_class" {
  description = "RDS PostgreSQL instance class for development."
  type        = string
  default     = "db.t4g.micro"
}

variable "database_allocated_storage" {
  description = "Allocated database storage in GiB."
  type        = number
  default     = 20

  validation {
    condition     = var.database_allocated_storage >= 20
    error_message = "database_allocated_storage must be at least 20 GiB for RDS PostgreSQL."
  }
}

variable "database_backup_retention_days" {
  description = "Automated backup retention in days for the development database."
  type        = number
  default     = 3

  validation {
    condition     = var.database_backup_retention_days >= 0 && var.database_backup_retention_days <= 35
    error_message = "database_backup_retention_days must be between 0 and 35."
  }
}

variable "api_cpu" {
  description = "API Fargate task CPU units."
  type        = number
  default     = 512

  validation {
    condition     = contains([256, 512, 1024], var.api_cpu)
    error_message = "api_cpu must be one of 256, 512, or 1024 for this development configuration."
  }
}

variable "api_memory" {
  description = "API Fargate task memory in MiB."
  type        = number
  default     = 1024

  validation {
    condition     = contains([512, 1024, 2048], var.api_memory)
    error_message = "api_memory must be one of 512, 1024, or 2048 for this development configuration."
  }
}

variable "frontend_cpu" {
  description = "Frontend Fargate task CPU units."
  type        = number
  default     = 256

  validation {
    condition     = contains([256, 512], var.frontend_cpu)
    error_message = "frontend_cpu must be 256 or 512 for this development configuration."
  }
}

variable "frontend_memory" {
  description = "Frontend Fargate task memory in MiB."
  type        = number
  default     = 512

  validation {
    condition     = contains([512, 1024], var.frontend_memory)
    error_message = "frontend_memory must be 512 or 1024 for this development configuration."
  }
}

variable "desired_api_task_count" {
  description = "Desired API ECS service task count when ECS services are enabled."
  type        = number
  default     = 1

  validation {
    condition     = var.desired_api_task_count >= 0
    error_message = "desired_api_task_count must not be negative."
  }
}

variable "desired_frontend_task_count" {
  description = "Desired frontend ECS service task count when ECS services are enabled."
  type        = number
  default     = 1

  validation {
    condition     = var.desired_frontend_task_count >= 0
    error_message = "desired_frontend_task_count must not be negative."
  }
}

variable "api_container_port" {
  description = "Port exposed by the backend API container."
  type        = number
  default     = 8000
}

variable "frontend_container_port" {
  description = "Port exposed by the nginx frontend container."
  type        = number
  default     = 80
}

variable "create_ecs_services" {
  description = "Create ECS task definitions and services. Keep false until Phase 18C supplies real image URIs."
  type        = bool
  default     = false
}

variable "api_image_uri" {
  description = "Commit-tagged backend image URI used by API, migration, and sync task definitions when ECS services are enabled."
  type        = string
  default     = ""
}

variable "frontend_image_uri" {
  description = "Commit-tagged frontend image URI used by the frontend task definition when ECS services are enabled."
  type        = string
  default     = ""
}

variable "log_retention_days" {
  description = "CloudWatch log retention in days for development task logs."
  type        = number
  default     = 14

  validation {
    condition     = contains([1, 3, 5, 7, 14, 30, 60, 90], var.log_retention_days)
    error_message = "log_retention_days must be a supported short retention value."
  }
}

variable "enable_ecs_container_insights" {
  description = "Enable ECS container insights. Disabled by default to keep development costs lower."
  type        = bool
  default     = false
}
