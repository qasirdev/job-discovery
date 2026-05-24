output "alb_dns_name" {
  value = aws_lb.alb.dns_name
}

output "ecs_cluster_name" {
  value = aws_ecs_cluster.cluster.name
}

output "secrets_manager_db_url_arn" {
  value = aws_secretsmanager_secret.db_url.arn
}

output "secrets_manager_supabase_url_arn" {
  value = aws_secretsmanager_secret.supabase_url.arn
}
