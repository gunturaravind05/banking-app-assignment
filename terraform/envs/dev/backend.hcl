bucket         = "banking-app-shared-terraform-state"
key            = "dev/terraform.tfstate"
region         = "ap-southeast-1"
dynamodb_table = "banking-app-shared-terraform-locks"
encrypt        = true