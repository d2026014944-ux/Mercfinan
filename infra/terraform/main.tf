provider "aws" {
  region = var.aws_region
}

locals {
  common_tags = merge({ Project = var.project_name }, var.tags)
}
