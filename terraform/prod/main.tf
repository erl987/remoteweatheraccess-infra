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

variable "project_id" {}
variable "region" {}
variable "database_version" {}
variable "sql_backup_region" {}
variable "database_tier" {}

provider "random" {}

# the credentials have to be provided in the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
provider "google" {
  project = var.project_id
  region = var.region
}

module "gcp_api_activation" {
  source = "../modules/gcp-api-activation"
  project_id = var.project_id
}

module "gcp_cloud_sql" {
  source = "../modules/gcp-cloud-sql"
  region = var.region
  database_version = var.database_version
  sql_backup_region = var.sql_backup_region
  database_tier = var.database_tier
  depends_on = [module.gcp_api_activation]
}

module "gcp_secret_manager" {
  source = "../modules/gcp-secret-manager"
  region = var.region
  user-db-password = module.gcp_cloud_sql.user-db-password
  weatherdata-db-password = module.gcp_cloud_sql.weatherdata-db-password
  depends_on = [module.gcp_api_activation]
}

module "gcp_service_accounts" {
  source = "../modules/gcp-service-accounts"
  project_id = var.project_id
}