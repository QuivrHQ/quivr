resource "aws_route53_zone" "this" {
  name = var.api_domain_name
}

resource "aws_acm_certificate" "this" {
  domain_name       = var.api_domain_name
  validation_method = "DNS"
}

resource "aws_route53_record" "validation" {
  for_each = {
    for dvo in aws_acm_certificate.this.domain_validation_options : dvo.domain_name => {
      name   = dvo.resource_record_name
      record = dvo.resource_record_value
      type   = dvo.resource_record_type
    }
  }

  name    = each.value.name
  records = [each.value.record]
  ttl     = 300
  type    = each.value.type
  zone_id = aws_route53_zone.this.zone_id
}

resource "aws_acm_certificate_validation" "this" {
  certificate_arn         = aws_acm_certificate.this.arn
  validation_record_fqdns = [for record in aws_route53_record.validation : record.fqdn]
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

