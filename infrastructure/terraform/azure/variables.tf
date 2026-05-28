variable "location" {
  description = "The Azure region to deploy to"
  type        = string
  default     = "uksouth"
}

variable "resource_group_name" {
  description = "The name of the resource group"
  type        = string
  default     = "rg-job-discovery-prod"
}

variable "prefix" {
  description = "The prefix used for all resources in this environment"
  type        = string
  default     = "jdprod"
}

variable "db_admin_user" {
  description = "The admin username for PostgreSQL"
  type        = string
  default     = "pgadmin"
}

variable "db_admin_password" {
  description = "The admin password for PostgreSQL"
  type        = string
  sensitive   = true
}
