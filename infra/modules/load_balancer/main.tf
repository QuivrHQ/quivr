resource "aws_route53_zone" "this" {
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


resource "aws_route53_record" "this" {
  zone_id = aws_route53_zone.this.zone_id
  name    = var.api_domain_name
  type    = "A"

  alias {
    name                   = aws_lb.this.dns_name
    zone_id                = aws_lb.this.zone_id
    evaluate_target_health = true
  }
  lifecycle {
    ignore_changes = [alias["name"]]
  }
}

