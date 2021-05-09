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
variable "gcp_project_id" {}
variable "gcp_region" {}
variable "gcp_database_version" {}
variable "gcp_sql_backup_region" {}
variable "gcp_database_tier" {}

provider "random" {}

# the credentials have to be provided in the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
provider "google" {
  project = var.gcp_project_id
  region = var.gcp_region
}

module "gcp_api_activation" {
  source = "../modules/gcp-api-activation"
  project_id = var.gcp_project_id
}

module "gcp_cloud_sql" {
  source = "../modules/gcp-cloud-sql"
  region = var.gcp_region
  database_version = var.gcp_database_version
  sql_backup_region = var.gcp_sql_backup_region
  database_tier = var.gcp_database_tier
  depends_on = [module.gcp_api_activation]
}

module "gcp_secret_manager" {
  source = "../modules/gcp-secret-manager"
  region = var.gcp_region
  user-db-password = module.gcp_cloud_sql.user-db-password
  weatherdata-db-password = module.gcp_cloud_sql.weatherdata-db-password
  depends_on = [module.gcp_api_activation]
}

module "gcp_service_accounts" {
  source = "../modules/gcp-service-accounts"
  project_id = var.gcp_project_id
}