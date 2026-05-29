variable "project_name" {
  type    = string
  default = "mercfinan"
}

variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "vpc_id" {
  type = string
}

variable "subnet_ids" {
  type = list(string)
}

variable "assign_public_ip" {
  type    = bool
  default = false
}

variable "api_allowed_cidrs" {
  type    = list(string)
  default = ["0.0.0.0/0"]
}

variable "api_image" {
  type = string
}

variable "worker_image" {
  type = string
}

variable "api_cpu" {
  type    = number
  default = 256
}

variable "api_memory" {
  type    = number
  default = 512
}

variable "worker_cpu" {
  type    = number
  default = 256
}

variable "worker_memory" {
  type    = number
  default = 512
}

variable "api_desired_count" {
  type    = number
  default = 1
}

variable "worker_desired_count" {
  type    = number
  default = 1
}

variable "api_environment" {
  type    = map(string)
  default = {}
}

variable "worker_environment" {
  type    = map(string)
  default = {}
}

variable "api_secrets" {
  type    = map(string)
  default = {}
}

variable "worker_secrets" {
  type    = map(string)
  default = {}
}

variable "api_secret_names" {
  type    = map(string)
  default = {}
}

variable "worker_secret_names" {
  type    = map(string)
  default = {}
}

variable "model_s3_bucket" {
  type    = string
  default = "meu-projeto-modelos-prod"
}

variable "model_s3_prefix" {
  type    = string
  default = ""
}

variable "secrets_manager_arns" {
  type    = list(string)
  default = []
}

variable "log_retention_days" {
  type    = number
  default = 14
}

variable "tags" {
  type    = map(string)
  default = {}
}
