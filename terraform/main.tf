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

# provided as environment variables `TF_VAR_GCP_PROJECT_ID`, etc. in Gitlab
variable "GCP_PROJECT_ID" {
  description = "The GCP project id where the application will be deployed"
}
variable "GCP_REGION" {
  description = "The GCP region where the application will be deployed"
  type = string
}
variable "GCP_DATABASE_VERSION" {
  description = "The Postgres database version for the weather database. The choice depends on the availability in GCP"
  type = string
}
variable "GCP_SQL_BACKUP_REGION" {
  description = "GCP region (or multi-region) for the database backup"
  type = string
}
variable "GCP_DATABASE_TIER" {
  description = "The machine type used for the database. Must be a GCP-machine type available for Cloud SQL"
  type = string
}

provider "random" {}

# the credentials have to be provided in the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
provider "google" {
  project = var.GCP_PROJECT_ID
  region = var.GCP_REGION
}

module "gcp_api_activation" {
  source = "./modules/gcp-api-activation"
  project_id = var.GCP_PROJECT_ID
}

module "gcp_cloud_sql" {
  source = "./modules/gcp-cloud-sql"
  region = var.GCP_REGION
  database_version = var.GCP_DATABASE_VERSION
  sql_backup_region = var.GCP_SQL_BACKUP_REGION
  database_tier = var.GCP_DATABASE_TIER
  depends_on = [module.gcp_api_activation]
}

module "gcp_secret_manager" {
  source = "./modules/gcp-secret-manager"
  region = var.GCP_REGION
  user-db-password = module.gcp_cloud_sql.user-db-password
  weatherdata-db-password = module.gcp_cloud_sql.weatherdata-db-password
  depends_on = [module.gcp_api_activation]
}

module "gcp_service_accounts" {
  source = "./modules/gcp-service-accounts"
  project_id = var.GCP_PROJECT_ID
}