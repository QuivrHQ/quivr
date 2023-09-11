resource "aws_ecs_service" "this" {
  name                               = var.service_name
  cluster                            = var.cluster_id
  task_definition                    = aws_ecs_task_definition.quivr-backend.arn
  deployment_maximum_percent         = var.deployment_maximum_percent
  deployment_minimum_healthy_percent = var.deployment_minimum_healthy_percent
  desired_count                      = var.desired_count
  enable_ecs_managed_tags            = var.enable_ecs_managed_tags
  enable_execute_command             = var.enable_execute_command
  health_check_grace_period_seconds  = var.health_check_grace_period_seconds
  iam_role                           = var.iam_role
  platform_version                   = var.platform_version
  propagate_tags                     = var.propagate_tags
  scheduling_strategy                = var.scheduling_strategy

  dynamic "capacity_provider_strategy" {
    for_each = var.capacity_provider_strategies
    content {
      capacity_provider = capacity_provider_strategy.value.capacity_provider
      weight            = capacity_provider_strategy.value.weight
      base              = capacity_provider_strategy.value.base
    }
  }

  deployment_circuit_breaker {
    enable   = var.deployment_circuit_breaker.enable
    rollback = var.deployment_circuit_breaker.rollback
  }

  deployment_controller {
    type = var.deployment_controller.type
  }

  load_balancer {

    target_group_arn = aws_lb_target_group.this.arn
    container_name   = var.name_task
    container_port   = var.port

  }

  network_configuration {
    subnets          = var.network_configuration.subnets
    security_groups  = var.network_configuration.security_groups
    assign_public_ip = var.network_configuration.assign_public_ip
  }

  lifecycle {
    ignore_changes = [task_definition]
  }
}

resource "aws_ecs_task_definition" "quivr-backend" {
  family                   = var.name_task
  network_mode             = "awsvpc"
  cpu                      = var.cpu
  memory                   = var.memory
  requires_compatibilities = ["FARGATE"]
  task_role_arn            = var.task_role_arn
  execution_role_arn       = var.execution_role_arn

  container_definitions = jsonencode([
    {
      name      = var.name_task
      image     = var.image
      cpu       = var.cpu
      memory    = var.memory
      essential = true
      command   = var.command
      environmentFiles = [
        {
          type  = "s3"
          value = var.env_file
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-create-group  = "true"
          awslogs-group         = var.awslogs_group
          awslogs-region        = var.awslogs_region
          awslogs-stream-prefix = var.awslogs_stream_prefix
        }
      }
      portMappings = [
        {
          containerPort = 5050
          hostPort      = 5050
          protocol      = "tcp"
          appProtocol   = "http"
          name          = "${var.name_task}-5050-tcp"
        }
      ]
    }
  ])

  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
  tags = {}
}


resource "aws_lb_target_group" "this" {
  name                   = var.name_task
  port                   = 80
  protocol               = "HTTP"
  vpc_id                 = var.vpc_id
  connection_termination = false
  deregistration_delay   = 300
  health_check {
    healthy_threshold   = 2
    unhealthy_threshold = 5
    timeout             = 25
    interval            = 30
    matcher             = "200"
    path                = "/"
    port                = "traffic-port"
    protocol            = "HTTP"
  }

  stickiness {
    enabled         = false
    type            = "lb_cookie"
    cookie_duration = 86400
  }

  target_type = "ip"
}

