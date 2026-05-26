terraform {
  required_version = "~> 1.15.4"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.74.0"
    }
  }
}

provider "azurerm" {
  features {
    key_vault {
      purge_soft_delete_on_destroy    = true
      recover_soft_deleted_key_vaults = true
    }
  }
}

data "azurerm_client_config" "current" {}

resource "azurerm_resource_group" "rg" {
  name     = "rg-${var.project_name}-${var.environment}"
  location = var.location
}

resource "azurerm_user_assigned_identity" "umi" {
  name                = "umi-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
}

resource "azurerm_container_registry" "acr" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  sku                 = "Basic"
  admin_enabled       = false
}

resource "azurerm_role_assignment" "acr_pull" {
  scope                = azurerm_container_registry.acr.id
  role_definition_name = "AcrPull"
  principal_id         = azurerm_user_assigned_identity.umi.principal_id
}

resource "azurerm_key_vault" "kv" {
  name                       = var.key_vault_name
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  tenant_id                  = data.azurerm_client_config.current.tenant_id
  sku_name                   = "standard"
  soft_delete_retention_days = 7

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = data.azurerm_client_config.current.object_id

    secret_permissions = [
      "Get", "List", "Set", "Delete", "Recover", "Backup", "Restore", "Purge"
    ]
  }

  access_policy {
    tenant_id = data.azurerm_client_config.current.tenant_id
    object_id = azurerm_user_assigned_identity.umi.principal_id

    secret_permissions = [
      "Get", "List"
    ]
  }
}

resource "azurerm_log_analytics_workspace" "law" {
  name                = "law-${var.project_name}-${var.environment}"
  location            = azurerm_resource_group.rg.location
  resource_group_name = azurerm_resource_group.rg.name
  sku                 = "PerGB2018"
  retention_in_days   = 30
}

resource "azurerm_container_app_environment" "env" {
  name                       = "cae-${var.project_name}-${var.environment}"
  location                   = azurerm_resource_group.rg.location
  resource_group_name        = azurerm_resource_group.rg.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.law.id
}

resource "azurerm_container_app" "app" {
  name                         = "ca-${var.project_name}-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.umi.id]
  }

  registry {
    server   = azurerm_container_registry.acr.login_server
    identity = azurerm_user_assigned_identity.umi.id
  }

  template {
    min_replicas = 1
    max_replicas = 5
    container {
      name   = var.app_name
      image  = "${azurerm_container_registry.acr.login_server}/${var.app_name}:${var.image_tag}"
      cpu    = 0.5
      memory = "1.0Gi"

      env {
        name  = "DATABASE_URL"
        value = "secretref:db-url"
      }
      
      env {
        name  = "SUPABASE_URL"
        value = "secretref:supabase-url"
      }
    }
  }

  secret {
    name                = "db-url"
    key_vault_secret_id = "https://${azurerm_key_vault.kv.name}.vault.azure.net/secrets/DATABASE_URL"
    identity            = azurerm_user_assigned_identity.umi.id
  }

  secret {
    name                = "supabase-url"
    key_vault_secret_id = "https://${azurerm_key_vault.kv.name}.vault.azure.net/secrets/SUPABASE_URL"
    identity            = azurerm_user_assigned_identity.umi.id
  }

  ingress {
    allow_insecure_connections = false
    external_enabled           = true
    target_port                = 80
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

resource "azurerm_container_app" "ranking_worker" {
  name                         = "ca-${var.project_name}-ranking-${var.environment}"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.rg.name
  revision_mode                = "Single"

  identity {
    type         = "UserAssigned"
    identity_ids = [azurerm_user_assigned_identity.umi.id]
  }

  registry {
    server   = azurerm_container_registry.acr.login_server
    identity = azurerm_user_assigned_identity.umi.id
  }

  template {
    min_replicas = 0
    max_replicas = 10
    container {
      name   = "${var.app_name}-ranking-worker"
      image  = "${azurerm_container_registry.acr.login_server}/${var.app_name}:${var.image_tag}"
      cpu    = 1.0
      memory = "2.0Gi"

      command = ["uv", "run", "python", "-m", "backend.agents.ranking.worker"]

      env {
        name  = "DATABASE_URL"
        value = "secretref:db-url"
      }
      
      env {
        name  = "SUPABASE_URL"
        value = "secretref:supabase-url"
      }
    }
  }

  secret {
    name                = "db-url"
    key_vault_secret_id = "https://${azurerm_key_vault.kv.name}.vault.azure.net/secrets/DATABASE_URL"
    identity            = azurerm_user_assigned_identity.umi.id
  }

  secret {
    name                = "supabase-url"
    key_vault_secret_id = "https://${azurerm_key_vault.kv.name}.vault.azure.net/secrets/SUPABASE_URL"
    identity            = azurerm_user_assigned_identity.umi.id
  }
}
