output "resource_group_name" {
  value = azurerm_resource_group.rg.name
}

output "container_app_url" {
  value = azurerm_container_app.app.latest_revision_fqdn
}

output "key_vault_uri" {
  value = azurerm_key_vault.kv.vault_uri
}

output "managed_identity_client_id" {
  value = azurerm_user_assigned_identity.umi.client_id
}
