output "backend_url" {
  description = "The FQDN of the Backend Container App"
  value       = "https://${azurerm_container_app.backend.ingress[0].fqdn}"
}

output "frontend_url" {
  description = "The FQDN of the Frontend Container App"
  value       = "https://${azurerm_container_app.frontend.ingress[0].fqdn}"
}
