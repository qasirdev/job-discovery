output "lb_dns_name" {
  value = aws_lb.alb.dns_name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.cluster.name
}

output "task_definition_arn" {
  value = aws_ecs_task_definition.app.arn
}

output "ecr_repository_url" {
  value = aws_ecr_repository.ecr.repository_url
}
