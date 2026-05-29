data "aws_iam_policy_document" "task_assume_role" {
  statement {
    actions = ["sts:AssumeRole"]

    principals {
      type        = "Service"
      identifiers = ["ecs-tasks.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "task_execution" {
  name               = "${var.project_name}-ecs-exec"
  assume_role_policy = data.aws_iam_policy_document.task_assume_role.json
  tags               = local.common_tags
}

resource "aws_iam_role_policy_attachment" "task_execution" {
  role       = aws_iam_role.task_execution.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}

resource "aws_iam_role" "task_role" {
  name               = "${var.project_name}-ecs-task"
  assume_role_policy = data.aws_iam_policy_document.task_assume_role.json
  tags               = local.common_tags
}

locals {
  model_prefix      = trim(var.model_s3_prefix, "/")
  model_object_path = local.model_prefix == "" ? "*" : "${local.model_prefix}/*"
}

data "aws_iam_policy_document" "task_access" {
  statement {
    actions = [
      "s3:GetObject",
      "s3:ListBucket",
    ]

    resources = [
      "arn:aws:s3:::${var.model_s3_bucket}",
      "arn:aws:s3:::${var.model_s3_bucket}/${local.model_object_path}",
    ]
  }

  dynamic "statement" {
    for_each = length(local.secrets_manager_merged) > 0 ? [1] : []

    content {
      actions = [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret",
      ]

      resources = local.secrets_manager_merged
    }
  }
}

resource "aws_iam_policy" "task_access" {
  name   = "${var.project_name}-task-access"
  policy = data.aws_iam_policy_document.task_access.json
  tags   = local.common_tags
}

resource "aws_iam_role_policy_attachment" "task_access" {
  role       = aws_iam_role.task_role.name
  policy_arn = aws_iam_policy.task_access.arn
}
