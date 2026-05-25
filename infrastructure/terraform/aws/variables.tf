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

variable "ecr_image_uri" {
  type        = string
  description = "The ECR image URI"
}

variable "desired_count" {
  type    = number
  default = 1
}
