terraform {
  required_providers {
    google = {
      source = "hashicorp/google"
      version = "3.66.1"
    }

    random = {
      source = "hashicorp/random"
      version = "3.1.0"
    }
  }

  backend "http" {
  }
}

# provided as environment variables `TF_VAR_gcp_project_id`, etc. in Gitlab
variable "gcp_project_id" {
  description = "The GCP project id where the application will be deployed"
}
variable "gcp_region" {
  description = "The GCP region where the application will be deployed"
  type = string
}
variable "gcp_database_version" {
  description = "The Postgres database version for the weather database. The choice depends on the availability in GCP"
  type = string
}
variable "gcp_sql_backup_region" {
  description = "GCP region (or multi-region) for the database backup"
  type = string
}
variable "gcp_database_tier" {
  description = "The machine type used for the database. Must be a GCP-machine type available for Cloud SQL"
  type = string
}

provider "random" {}

# the credentials have to be provided in the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
provider "google" {
  project = var.gcp_project_id
  region = var.gcp_region
}

module "gcp_api_activation" {
  source = "./modules/gcp-api-activation"
  project_id = var.gcp_project_id
}

module "gcp_cloud_sql" {
  source = "./modules/gcp-cloud-sql"
  region = var.gcp_region
  database_version = var.gcp_database_version
  sql_backup_region = var.gcp_sql_backup_region
  database_tier = var.gcp_database_tier
  depends_on = [module.gcp_api_activation]
}

module "gcp_secret_manager" {
  source = "./modules/gcp-secret-manager"
  region = var.gcp_region
  user-db-password = module.gcp_cloud_sql.user-db-password
  weatherdata-db-password = module.gcp_cloud_sql.weatherdata-db-password
  depends_on = [module.gcp_api_activation]
}

module "gcp_service_accounts" {
  source = "./modules/gcp-service-accounts"
  project_id = var.gcp_project_id
}