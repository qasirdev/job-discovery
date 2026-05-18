output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "container_app_env_id" {
  value = azurerm_container_app_environment.env.id
}
