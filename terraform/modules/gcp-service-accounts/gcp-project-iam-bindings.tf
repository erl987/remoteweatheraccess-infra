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

resource "google_secret_manager_secret_iam_member" "weather-db-password-secret-backend-service-account-binding" {
  project   = var.project_id
  secret_id = var.weather-db-password-secret-id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend-service-account.email}"
}

resource "google_secret_manager_secret_iam_member" "user-db-password-secret-backend-service-account-binding" {
  project   = var.project_id
  secret_id = var.user-db-password-secret-id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend-service-account.email}"
}

resource "google_secret_manager_secret_iam_member" "jwt-secret-key-secret-backend-service-account-binding" {
  project   = var.project_id
  secret_id = var.jwt-secret-key-secret-id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.backend-service-account.email}"
}

resource "google_secret_manager_secret_iam_member" "frontend-db-password-secret-frontend-service-account-binding" {
  project   = var.project_id
  secret_id = var.frontend-db-password-secret-id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.frontend-service-account.email}"
}

resource "google_secret_manager_secret_iam_member" "frontend-db-password-secret-cloud-build-service-account-binding" {
  project   = var.project_id
  secret_id = var.frontend-db-password-secret-id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
}

resource "google_secret_manager_secret_iam_member" "frontend-settings-secret-frontend-service-account-binding" {
  project   = var.project_id
  secret_id = var.frontend-settings-secret-id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${google_service_account.frontend-service-account.email}"
}

resource "google_secret_manager_secret_iam_member" "frontend-settings-secret-cloud-build-service-account-binding" {
  project   = var.project_id
  secret_id = var.frontend-settings-secret-id
  role      = "roles/secretmanager.secretAccessor"
  member    = "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
}

resource "google_project_iam_binding" "service-account-sql-client-role" {
  project = var.project_id
  role    = "roles/cloudsql.client"

  members = [
    "serviceAccount:${google_service_account.backend-service-account.email}",
    "serviceAccount:${google_service_account.frontend-service-account.email}",
    "serviceAccount:${var.project_number}@cloudbuild.gserviceaccount.com"
  ]
}

resource "google_storage_bucket_iam_member" "exporter-bucket-exporter-service-account-binding" {
  bucket = var.export_data_bucket_name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.exporter-service-account.email}"
}

resource "google_storage_bucket_iam_member" "exporter-bucket-frontend-service-account-binding" {
  bucket = var.export_data_bucket_name
  role   = "roles/storage.objectViewer"
  member = "serviceAccount:${google_service_account.frontend-service-account.email}"
}

resource "google_project_iam_binding" "service-account-cloud-run-viewer-role" {
  project = var.project_id
  role    = "roles/run.viewer"

  members = [
    "serviceAccount:${google_service_account.frontend-service-account.email}"
  ]
}

resource "google_storage_bucket_iam_binding" "public-cloud-frontend-static-storage-role" {
  bucket = var.frontend_static_bucket_name
  role   = "roles/storage.objectViewer"

  members = [
    "allUsers"
  ]
}

resource "google_project_iam_binding" "frontend-log-writer-role" {
  project = var.project_id
  role    = "roles/logging.logWriter"

  members = [
    "serviceAccount:${google_service_account.frontend-service-account.email}",
  ]
}
