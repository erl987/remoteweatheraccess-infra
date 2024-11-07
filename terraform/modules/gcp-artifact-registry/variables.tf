variable "project_id" {
  description = "The GCP project where the application will be deployed"
  type        = string
}

variable "region" {
  description = "The GCP region where the application will be deployed"
  type        = string
}

variable "frontend_region" {
  description = "The GCP region where the frontend will be deployed"
  type        = string
}
