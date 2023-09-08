resource "aws_route53_zone" "api" {
  name = var.api_domain_name
}


resource "aws_lb" "this" {
  name               = "quivr"
  internal           = false
  load_balancer_type = "application"
  security_groups    = ["sg-0aaabded23c30cdc3"]
  subnets            = [for subnet in var.subnets : subnet.id]

  enable_deletion_protection = true



  tags = {
    Environment = "production"
  }
}


