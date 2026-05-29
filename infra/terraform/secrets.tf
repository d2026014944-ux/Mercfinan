data "aws_secretsmanager_secret" "api" {
  for_each = var.api_secret_names
  name     = each.value
}

data "aws_secretsmanager_secret" "worker" {
  for_each = var.worker_secret_names
  name     = each.value
}

locals {
  api_secret_arns          = { for name, secret in data.aws_secretsmanager_secret.api : name => secret.arn }
  worker_secret_arns       = { for name, secret in data.aws_secretsmanager_secret.worker : name => secret.arn }
  api_secrets_merged       = merge(var.api_secrets, local.api_secret_arns)
  worker_secrets_merged    = merge(var.worker_secrets, local.worker_secret_arns)
  secrets_manager_merged   = distinct(concat(var.secrets_manager_arns, values(local.api_secret_arns), values(local.worker_secret_arns)))
}
