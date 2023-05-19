#  Remote Weather Access - Client/server solution for distributed weather networks
#   Copyright (C) 2013-2023 Ralf Rettig (info@personalfme.de)
#
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU Affero General Public License as
#   published by the Free Software Foundation, either version 3 of the
#   License, or (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU Affero General Public License for more details.
#
#   You should have received a copy of the GNU Affero General Public License
#   along with this program.  If not, see <https://www.gnu.org/licenses/>.

terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "3.66.1"
    }

    random = {
      source  = "hashicorp/random"
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
variable "GCP_PROJECT_NUMBER" {
  description = "The GCP project number where the application will be deployed"
}
variable "GCP_REGION" {
  description = "The GCP region where the application will be deployed"
  type        = string
}
variable "GCP_DATABASE_VERSION" {
  description = "The Postgres database version for the weather database. The choice depends on the availability in GCP"
  type        = string
}
variable "GCP_SQL_BACKUP_REGION" {
  description = "GCP region (or multi-region) for the database backup"
  type        = string
}
variable "GCP_DATABASE_TIER" {
  description = "The machine type used for the database. Must be a GCP-machine type available for Cloud SQL"
  type        = string
}

provider "random" {}

# the credentials have to be provided in the environment variable `GOOGLE_APPLICATION_CREDENTIALS`
provider "google" {
  project = var.GCP_PROJECT_ID
  region  = var.GCP_REGION
}

module "gcp_api_activation" {
  source     = "./modules/gcp-api-activation"
  project_id = var.GCP_PROJECT_ID
}

module "gcp_app_engine" {
  source     = "./modules/gcp-app-engine"
  region     = var.GCP_REGION
  project_id = var.GCP_PROJECT_ID
}

module "gcp_cloud_sql" {
  source            = "./modules/gcp-cloud-sql"
  region            = var.GCP_REGION
  database_version  = var.GCP_DATABASE_VERSION
  sql_backup_region = var.GCP_SQL_BACKUP_REGION
  database_tier     = var.GCP_DATABASE_TIER
  depends_on        = [module.gcp_api_activation]
}

module "gcp_secret_manager" {
  source                  = "./modules/gcp-secret-manager"
  region                  = var.GCP_REGION
  user-db-password        = module.gcp_cloud_sql.user-db-password
  weatherdata-db-password = module.gcp_cloud_sql.weatherdata-db-password
  frontend-db-password    = module.gcp_cloud_sql.frontend-db-password
  depends_on              = [module.gcp_api_activation]
}

module "gcp_cloud_storage" {
  source     = "./modules/gcp-cloud-storage"
  region     = var.GCP_REGION
  project_id = var.GCP_PROJECT_ID
  depends_on = [module.gcp_api_activation]
}

module "gcp_service_accounts" {
  source                         = "./modules/gcp-service-accounts"
  project_id                     = var.GCP_PROJECT_ID
  project_number                 = var.GCP_PROJECT_NUMBER
  export_data_bucket_name        = module.gcp_cloud_storage.export-data-bucket-name
  frontend_static_bucket_name    = module.gcp_cloud_storage.frontend-static-bucket-name
  frontend-settings-secret-id    = module.gcp_secret_manager.frontend-settings-secret-id
  frontend-db-password-secret-id = module.gcp_secret_manager.frontend-db-password-secret-id
  user-db-password-secret-id     = module.gcp_secret_manager.user-db-password-secret-id
  weather-db-password-secret-id  = module.gcp_secret_manager.weather-db-password-secret-id
  jwt-secret-key-secret-id       = module.gcp_secret_manager.jwt-secret-key-secret-id
}