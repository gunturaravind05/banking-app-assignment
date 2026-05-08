output "environment" {
  value = var.environment
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "public_subnet_ids" {
  value = module.vpc.public_subnet_ids
}

output "private_app_subnet_ids" {
  value = module.vpc.private_app_subnet_ids
}

output "private_db_subnet_ids" {
  value = module.vpc.private_db_subnet_ids
}

output "alb_sg_id" {
  value = module.security_group.alb_sg_id
}

output "app_sg_id" {
  value = module.security_group.app_sg_id
}

output "rds_sg_id" {
  value = module.security_group.rds_sg_id
}

output "alb_dns_name" {
  value = module.alb.alb_dns_name
}

output "target_group_arn" {
  value = module.alb.target_group_arn
}

output "ecr_repository_url" {
  value = module.ecr.repository_url
}

output "db_endpoint" {
  value = module.rds.db_endpoint
}

output "codebuild_project_name" {
  value = module.codebuild.codebuild_project_name
}

output "pipeline_name" {
  value = module.codepipeline.pipeline_name
}

output "github_connection_arn" {
  value = module.codepipeline.github_connection_arn
}