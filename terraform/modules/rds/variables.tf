variable "project_name" {}
variable "environment" {}

variable "private_db_subnet_ids" {
  type = list(string)
}

variable "rds_sg_id" {}

variable "db_username" {
  default = "admin"
}

variable "db_password" {
  sensitive = true
}

variable "db_name" {
  default = "bankdb"
}