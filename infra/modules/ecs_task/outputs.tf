

output "task_definition_arn" {
  description = "The ARN of the ECS task definition."
  value       = aws_ecs_task_definition.quivr-backend.arn
}
