resource "aws_route53_zone" "api" {
  name = var.api_domain_name
}


data "aws_vpc" "selected" {
  id = "vpc-005115b22b9dd01b0"
}

data "aws_subnets" "example" {
  filter {
    name   = "vpc-id"
    values = ["vpc-005115b22b9dd01b0"]
  }
}

data "aws_subnet" "example" {
  for_each = toset(data.aws_subnets.example.ids)
  id       = each.value
}


resource "aws_lb" "this" {
  name               = "quivr"
  internal           = false
  load_balancer_type = "application"
  security_groups    = ["sg-0aaabded23c30cdc3"]
  subnets            = [for subnet in data.aws_subnet.example : subnet.id]

  enable_deletion_protection = true



  tags = {
    Environment = "production"
  }
}


