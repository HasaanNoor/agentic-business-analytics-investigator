#!/bin/sh
set -e

ROOT_DIR="$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)"
TERRAFORM_ROOT="$ROOT_DIR/infrastructure/terraform"
DEV_DIR="$TERRAFORM_ROOT/environments/dev"

echo "Checking Terraform formatting..."
terraform fmt -check -recursive "$TERRAFORM_ROOT"

echo "Initializing Terraform without a backend..."
cd "$DEV_DIR"
terraform init -backend=false

echo "Validating Terraform configuration..."
terraform validate

echo "Terraform validation completed."
