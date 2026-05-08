variable "aws_region" {
  default = "ap-southeast-1"
}

variable "environment" {
  default = "dev"
}

variable "project_name" {
  default = "banking-app"
}

variable "db_password" {
  sensitive = true
}