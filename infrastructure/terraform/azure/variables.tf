variable "project_name" {
  type    = string
  default = "jobdiscovery"
}

variable "environment" {
  type    = string
  default = "prod"
}

variable "location" {
  type    = string
  default = "East US"
}

variable "docker_image" {
  type        = string
  description = "The Docker image to deploy"
  default     = "ghcr.io/qasirmehmood/job-discovery:latest"
}

variable "acr_name" {
  type    = string
  default = "acrjobdiscovery"
}

variable "app_name" {
  type    = string
  default = "job-discovery-app"
}

variable "image_tag" {
  type    = string
  default = "latest"
}

variable "key_vault_name" {
  type    = string
  default = "kvjobdiscoveryprod"
}
