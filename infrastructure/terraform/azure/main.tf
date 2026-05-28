terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.74.0"
    }
  }
}

provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "job_discovery_rg" {
  name     = var.resource_group_name
  location = var.location
}

# PostgreSQL Database (Flexible Server)
resource "azurerm_postgresql_flexible_server" "db" {
  name                   = "${var.prefix}-postgres"
  resource_group_name    = azurerm_resource_group.job_discovery_rg.name
  location               = azurerm_resource_group.job_discovery_rg.location
  version                = "14"
  administrator_login    = var.db_admin_user
  administrator_password = var.db_admin_password
  zone                   = "1"
  storage_mb             = 32768
  sku_name               = "B_Standard_B1ms"
}

# Redis Cache
resource "azurerm_redis_cache" "redis" {
  name                = "${var.prefix}-redis"
  location            = azurerm_resource_group.job_discovery_rg.location
  resource_group_name = azurerm_resource_group.job_discovery_rg.name
  capacity            = 0
  family              = "C"
  sku_name            = "Basic"
  enable_non_ssl_port = false
}

# Container App Environment
resource "azurerm_container_app_environment" "env" {
  name                = "${var.prefix}-env"
  location            = azurerm_resource_group.job_discovery_rg.location
  resource_group_name = azurerm_resource_group.job_discovery_rg.name
}

# Backend Container App
resource "azurerm_container_app" "backend" {
  name                         = "${var.prefix}-backend"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.job_discovery_rg.name
  revision_mode                = "Single"

  template {
    min_replicas = 0
    max_replicas = 5

    container {
      name   = "backend"
      image  = "ghcr.io/yourorg/job-discovery-backend:latest"
      cpu    = 1.0
      memory = "2Gi"

      env {
        name  = "DATABASE_URL"
        value = "postgresql+asyncpg://${var.db_admin_user}:${var.db_admin_password}@${azurerm_postgresql_flexible_server.db.fqdn}:5432/postgres"
      }
      env {
        name  = "REDIS_URL"
        value = "rediss://:${azurerm_redis_cache.redis.primary_access_key}@${azurerm_redis_cache.redis.hostname}:${azurerm_redis_cache.redis.ssl_port}"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8000
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}

# Frontend Container App
resource "azurerm_container_app" "frontend" {
  name                         = "${var.prefix}-frontend"
  container_app_environment_id = azurerm_container_app_environment.env.id
  resource_group_name          = azurerm_resource_group.job_discovery_rg.name
  revision_mode                = "Single"

  template {
    min_replicas = 0
    max_replicas = 5

    container {
      name   = "frontend"
      image  = "ghcr.io/yourorg/job-discovery-frontend:latest"
      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "NEXT_PUBLIC_API_URL"
        value = "https://${azurerm_container_app.backend.ingress[0].fqdn}"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 3000
    traffic_weight {
      percentage      = 100
      latest_revision = true
    }
  }
}
