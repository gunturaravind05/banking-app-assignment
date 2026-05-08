variable "project_name" {}
variable "environment" {}

variable "vpc_id" {}

variable "public_subnet_ids" {
  type = list(string)
}

variable "alb_sg_id" {}

variable "app_port" {
  default = 8080
}