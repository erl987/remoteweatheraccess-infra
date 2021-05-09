# input variable definitions

variable "region" {
  description = "The GCP region where the application will be deployed"
  type = string
}

variable "database_version" {
  description = "The Postgres database version for the weather database. The choice depends on the availability in GCP"
  type = string
}

variable "sql_backup_region" {
  description = "GCP region (or multi-region) for the database backup"
  type = string
}

variable "database_tier" {
  description = "The machine type used for the database. Must be a GCP-machine type available for Cloud SQL"
  type = string
}
