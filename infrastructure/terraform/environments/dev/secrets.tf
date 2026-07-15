resource "aws_secretsmanager_secret" "database_url" {
  name        = local.database_secret_name
  description = "SQLAlchemy DATABASE_URL for the ${local.name_prefix} API and backend one-off tasks"

  tags = {
    Name = local.database_secret_name
  }
}

resource "aws_secretsmanager_secret_version" "database_url" {
  secret_id     = aws_secretsmanager_secret.database_url.id
  secret_string = local.database_url
}
