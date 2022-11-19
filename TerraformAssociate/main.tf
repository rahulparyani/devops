terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "4.40.0"
    }
  }
}

provider "aws" {
  # Configuration options
  region = "us-east-1"
}

resource "aws_instance" "my-web" {
  ami           = "ami-026b57f3c383c2eec"
  instance_type = "t2.micro"
  tags = {
    Name = "MyWebServer"
  }
}