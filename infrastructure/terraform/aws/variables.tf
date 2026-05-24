variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "project_name" {
  type    = string
  default = "jobdiscovery"
}

variable "environment" {
  type    = string
  default = "prod"
}

variable "docker_image" {
  type        = string
  description = "The Docker image to deploy"
  default     = "ghcr.io/qasirmehmood/job-discovery:latest"
}
