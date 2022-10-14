terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_vpc" "my-vpc" {
  cidr_block = "10.10.0.0/16"
  enable_dns_hostnames = true
  tags = {
    "Name" = "MyVPC"
  }
}

resource "aws_subnet" "my-public-subnet" {
  cidr_block                                  = "10.10.1.0/24"
  vpc_id                                      = aws_vpc.my-vpc.id
  map_public_ip_on_launch                     = true
  enable_resource_name_dns_a_record_on_launch = true
  availability_zone                           = "us-east-1a"
}

resource "aws_internet_gateway" "my-ig" {
  vpc_id = aws_vpc.my-vpc.id
  tags = {
    name = "my-ig"
  }
}

resource "aws_route_table" "my-aws_route_table" {
  vpc_id = aws_vpc.my-vpc.id
  route {
    cidr_block                 = "0.0.0.0/0"
    gateway_id                 = aws_internet_gateway.my-ig.id
  }
}

resource "aws_route_table_association" "my-association" {
  route_table_id = aws_route_table.my-aws_route_table.id
  subnet_id      = aws_subnet.my-public-subnet.id
}

resource "aws_security_group" "my-sg" {
  vpc_id      = aws_vpc.my-vpc.id
  name        = "my-sg"
  description = "sg created by terra"
  ingress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = "internet on 80"
    from_port        = 80
    protocol         = "tcp"
    to_port          = 80
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    security_groups  = []
    self             = false
    }, {
    cidr_blocks      = ["49.34.232.11/32"]
    description      = "SSH on my IP"
    from_port        = 22
    to_port          = 22
    protocol         = "tcp"
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    security_groups  = []
    self             = false
    }
  ]
  egress = [{
    cidr_blocks      = ["0.0.0.0/0"]
    description      = "internet acess"
    from_port        = 0
    protocol         = "-1"
    to_port          = 0
    ipv6_cidr_blocks = []
    prefix_list_ids  = []
    security_groups  = []
    self             = false
  }]
}

resource "aws_key_pair" "new-key" {
  key_name   = "new-key"
  public_key = file("publicKey.pub")
}

resource "aws_instance" "my-web" {
  ami             = "ami-026b57f3c383c2eec"
  instance_type   = "t2.micro"
  key_name        = aws_key_pair.new-key.id
  vpc_security_group_ids = [ aws_security_group.my-sg.id ]
  subnet_id       = aws_subnet.my-public-subnet.id
  user_data = file("user-data.sh")
}