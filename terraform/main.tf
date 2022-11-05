terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.23.0"
    }
  }
  # bucket and dynamodb_table are stored in backend.tfvars (in gitignore)
  backend "s3" {
    key    = "state/reddit.tfstate"
    region = "eu-west-1"
  }
}

provider "aws" {
  region = "eu-west-1"
}
