moved {
  from = module.ecs_cluster.aws_ecs_service.quivr-backend
  to   = module.quivr_backend.aws_ecs_service.quivr-backend
}

moved {
  from = module.ecs_cluster.aws_ecs_task_definition.quivr-backend
  to   = module.quivr_backend.aws_ecs_task_definition.quivr-backend
}

moved {
  from = module.quivr_backend.aws_ecs_service.quivr-backend
  to   = module.quivr_backend.aws_ecs_service.this
}

import {
  to = module.quivr_backend.aws_lb_target_group.this
  id = "arn:aws:elasticloadbalancing:eu-west-3:253053805092:targetgroup/quivr/25488c9954b3d630"
}
moved {
  from = module.api.aws_route53_zone.api
  to   = module.api.aws_route53_zone.this
}

import {
  to = module.api.aws_route53_record.this
  id = "Z075975614NR7YUNW2MOK_api.quivr.app_A"
}
