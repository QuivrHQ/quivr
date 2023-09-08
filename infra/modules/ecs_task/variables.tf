

variable "service_name" {
  description = "The name of the ECS service."
  type        = string
  default     = "quivr-backend"
}

variable "cluster_id" {
  description = "ECS cluster ID."
  type        = string
}

variable "deployment_maximum_percent" {
  description = "The maximum percent of tasks to deploy."
  type        = number
  default     = 200
}

variable "task_role_arn" {
  description = "The ARN of the task role."
  type        = string
  default     = "arn:aws:iam::253053805092:role/ecsTaskExecutionRole"
}

variable "execution_role_arn" {
  description = "The ARN of the execution role."
  type        = string
  default     = "arn:aws:iam::253053805092:role/ecsTaskExecutionRole"
}

# ... [similarly define other variables for the fields of the resources]

variable "capacity_provider_strategies" {
  description = "Capacity provider strategy to use for the service."
  type = list(object({
    base              = number
    capacity_provider = string
    weight            = number
  }))
  default = [
    {
      base              = 0
      capacity_provider = "FARGATE"
      weight            = 1
    },
    {
      base              = 1
      capacity_provider = "FARGATE_SPOT"
      weight            = 10
    }
  ]
}

variable "image" {
  description = "Container image URI."
  type        = string
  default     = "253053805092.dkr.ecr.eu-west-3.amazonaws.com/quivr:0c1a8a9cdd42807dd7a3650f1b59630680d55fe5"
}

variable "env_file" {
  description = "ARN for the environment file in S3."
  type        = string
  default     = "arn:aws:s3:::quivr-env-variables/production.env"
}

variable "awslogs_group" {
  description = "The name of the CloudWatch log group."
  type        = string
  default     = "/ecs/quivr"
}

variable "awslogs_region" {
  description = "The region for CloudWatch logs."
  type        = string
  default     = "eu-west-3"
}

variable "awslogs_stream_prefix" {
  description = "The stream prefix for CloudWatch logs."
  type        = string
  default     = "ecs"
}


variable "deployment_minimum_healthy_percent" {
  description = "The minimum healthy percent for deployments."
  type        = number
  default     = 50
}

variable "desired_count" {
  description = "The number of task instances to launch."
  type        = number
  default     = 4
}

variable "enable_ecs_managed_tags" {
  description = "Specifies whether to enable ECS managed tags for the tasks within the service."
  type        = bool
  default     = true
}

variable "enable_execute_command" {
  description = "Specifies whether to enable the execute command functionality for the tasks within the service."
  type        = bool
  default     = false
}

variable "health_check_grace_period_seconds" {
  description = "The period of time, in seconds, that the Amazon ECS service scheduler should ignore unhealthy Elastic Load Balancing target health checks after a task has first started."
  type        = number
  default     = 30
}

variable "iam_role" {
  description = "The IAM role that allows Amazon ECS to make calls to your load balancer on your behalf."
  type        = string
  default     = "/aws-service-role/ecs.amazonaws.com/AWSServiceRoleForECS"
}

variable "platform_version" {
  description = "The platform version on which to run your service."
  type        = string
  default     = "1.4.0"
}

variable "propagate_tags" {
  description = "Specifies whether to propagate the tags from the task definition or the service to the tasks."
  type        = string
  default     = "NONE"
}

variable "scheduling_strategy" {
  description = "The scheduling strategy to use for the service."
  type        = string
  default     = "REPLICA"
}

variable "deployment_circuit_breaker" {
  description = "Configuration for ECS service deployment circuit breaker"
  type = object({
    enable   = bool
    rollback = bool
  })
  default = {
    enable   = true
    rollback = true
  }
}

variable "deployment_controller" {
  description = "Configuration for ECS service deployment controller"
  type = object({
    type = string
  })
  default = {
    type = "ECS"
  }
}

variable "load_balancers" {
  description = "Configuration for load balancers"
  type = list(object({
    target_group_arn = string
    container_name   = string
    container_port   = number
  }))
  default = [{
    target_group_arn = "arn:aws:elasticloadbalancing:eu-west-3:253053805092:targetgroup/quivr/25488c9954b3d630"
    container_name   = "quivr"
    container_port   = 5050
  }]
}

variable "network_configuration" {
  description = "Network configuration for the ECS service"
  type = object({
    subnets          = list(string)
    security_groups  = list(string)
    assign_public_ip = bool
  })
  default = {
    assign_public_ip = true
    security_groups  = ["sg-0aaabded23c30cdc3"]
    subnets = [
      "subnet-011cb4af786747e14",
      "subnet-04f34d520204470aa",
      "subnet-05f5a63610b3a7eb9",
    ]
  }
}
