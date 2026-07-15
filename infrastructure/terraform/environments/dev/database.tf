resource "random_password" "database_password" {
  length  = 32
  special = false
}

resource "aws_db_subnet_group" "postgres" {
  name       = "${local.name_prefix}-db-subnets"
  subnet_ids = aws_subnet.private_db[*].id

  tags = {
    Name = "${local.name_prefix}-db-subnets"
  }
}

resource "aws_db_instance" "postgres" {
  identifier = local.db_name

  engine         = "postgres"
  engine_version = "16.3"
  instance_class = var.database_instance_class

  allocated_storage     = var.database_allocated_storage
  max_allocated_storage = var.database_allocated_storage + 20
  storage_type          = "gp3"
  storage_encrypted     = true

  db_name  = var.database_name
  username = var.database_username
  password = random_password.database_password.result
  port     = 5432

  db_subnet_group_name   = aws_db_subnet_group.postgres.name
  vpc_security_group_ids = [aws_security_group.database.id]
  publicly_accessible    = false

  backup_retention_period = var.database_backup_retention_days
  deletion_protection     = false
  multi_az                = false
  skip_final_snapshot     = true

  auto_minor_version_upgrade = true
  copy_tags_to_snapshot      = true

  tags = {
    Name = local.db_name
  }
}
