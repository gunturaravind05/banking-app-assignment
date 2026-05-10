module "vpc" {
  source = "../../modules/vpc"

  project_name = var.project_name
  environment  = var.environment

  vpc_cidr = "10.10.0.0/16"

  availability_zones = [
    "ap-southeast-1a",
    "ap-southeast-1b"
  ]

  public_subnets = [
    "10.10.1.0/24",
    "10.10.2.0/24"
  ]

  private_app_subnets = [
    "10.10.11.0/24",
    "10.10.12.0/24"
  ]

  private_db_subnets = [
    "10.10.21.0/24",
    "10.10.22.0/24"
  ]
}

module "security_group" {
  source = "../../modules/security-group"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
}

module "alb" {
  source = "../../modules/alb"

  project_name = var.project_name
  environment  = var.environment

  vpc_id            = module.vpc.vpc_id
  public_subnet_ids = module.vpc.public_subnet_ids

  alb_sg_id = module.security_group.alb_sg_id
}

module "ecr" {
  source = "../../modules/ecr"

  project_name = var.project_name
  environment  = var.environment
}

module "rds" {
  source = "../../modules/rds"

  project_name = var.project_name
  environment  = var.environment

  private_db_subnet_ids = module.vpc.private_db_subnet_ids

  rds_sg_id = module.security_group.rds_sg_id

  db_password = var.db_password
}

module "secrets" {
  source = "../../modules/secrets"

  project_name = var.project_name
  environment  = var.environment

  db_password = var.db_password
}

module "ecs" {
  source = "../../modules/ecs"

  project_name = var.project_name
  environment  = var.environment

  private_app_subnet_ids = module.vpc.private_app_subnet_ids

  app_sg_id        = module.security_group.app_sg_id
  target_group_arn = module.alb.target_group_arn

  ecr_repository_url = module.ecr.repository_url

  db_endpoint = module.rds.db_endpoint

  db_password_secret_arn = module.secrets.db_password_secret_arn

  db_password = var.db_password
}

module "codebuild" {
  source = "../../modules/codebuild"

  project_name = var.project_name
  environment  = var.environment
  aws_region   = var.aws_region

  ecr_repository_arn = module.ecr.repository_arn

  ecs_cluster_name = module.ecs.ecs_cluster_name
  ecs_service_name = "${var.project_name}-${var.environment}-service"
}

module "codepipeline" {
  source = "../../modules/codepipeline"

  project_name = var.project_name
  environment  = var.environment
  aws_region   = var.aws_region

  github_owner  = "gunturaravind05"
  github_repo   = "banking-app-assignment"
  github_branch = "main"

  codebuild_project_name = module.codebuild.codebuild_project_name
}

module "monitoring" {
  source = "../../modules/monitoring"

  project_name = var.project_name
  environment  = var.environment

  alb_arn_suffix          = module.alb.alb_arn_suffix
  target_group_arn_suffix = module.alb.target_group_arn_suffix

  ecs_cluster_name = module.ecs.ecs_cluster_name
  ecs_service_name = "${var.project_name}-${var.environment}-service"

  rds_identifier = module.rds.rds_identifier
}