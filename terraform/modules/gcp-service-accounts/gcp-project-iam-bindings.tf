#  Remote Weather Access - Client/server solution for distributed weather networks
#   Copyright (C) 2013-2021 Ralf Rettig (info@personalfme.de)
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

resource "google_project_iam_binding" "service-account-secret-accessor-role" {
  project = var.project_id
  role = "roles/secretmanager.secretAccessor"

  members = [
    "serviceAccount:${google_service_account.backend-service-account.email}"]
}

resource "google_project_iam_binding" "service-account-sql-client-role" {
  project = var.project_id
  role = "roles/cloudsql.client"

  members = [
    "serviceAccount:${google_service_account.backend-service-account.email}"]
}

resource "google_project_iam_binding" "service-account-cloud-storage-role" {
  project = var.project_id
  role = "roles/storage.admin"

  members = [
    "serviceAccount:${google_service_account.exporter-service-account.email}"]
}

resource "google_storage_bucket_iam_binding" "public-cloud-storage-role" {
  bucket = var.export_data_bucket_name
  role = "roles/storage.objectViewer"

  members = [
    "allUsers"]
}
