terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.67.0"
    }
  }


  required_version = ">= 1.0"
}

resource "aws_s3_bucket" "source_bucket" {
  bucket = "fga-source-bucket"

  tags = {
    Name        = "My source bucket"
    Environment = "Dev"
  }
}

provider "aws" {
  region  = "eu-west-1"
  profile = "BigSpark"
}
