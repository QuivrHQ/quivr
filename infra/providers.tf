provider "aws" {
  region = "eu-west-3"
}

terraform {
  backend "s3" {
    bucket = "terraform-state-quivr-prod"
    key    = "terraform.tfstate"
    region = "eu-west-3"
  }
}
