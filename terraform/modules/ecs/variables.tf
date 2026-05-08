variable "project_name" {}
variable "environment" {}

variable "private_app_subnet_ids" {
  type = list(string)
}

variable "app_sg_id" {}

variable "target_group_arn" {}

variable "ecr_repository_url" {}

variable "db_endpoint" {}

variable "db_username" {
  default = "admin"
}

variable "db_password" {
  sensitive = true
}

variable "container_port" {
  default = 8080
}