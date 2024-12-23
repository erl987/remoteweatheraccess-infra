#  Remote Weather Access - Client/server solution for distributed weather networks
#   Copyright (C) 2013-2024 Ralf Rettig (info@personalfme.de)
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

resource "google_project_service" "secret-manager-api" {
  project = var.project_id
  service = "secretmanager.googleapis.com"
}

resource "google_project_service" "artifact-registry-api" {
  project = var.project_id
  service = "artifactregistry.googleapis.com"
}

resource "google_project_service" "cloud-run-api" {
  project = var.project_id
  service = "run.googleapis.com"
}

resource "google_project_service" "cloud-sql-admin-api" {
  project = var.project_id
  service = "sqladmin.googleapis.com"
}

resource "google_project_service" "cloud-storage-api" {
  project = var.project_id
  service = "storage.googleapis.com"
}

resource "google_project_service" "app-engine-api" {
  project = var.project_id
  service = "appengine.googleapis.com"
}

resource "google_project_service" "cloud-scheduler-api" {
  project = var.project_id
  service = "cloudscheduler.googleapis.com"
}

resource "google_project_service" "cloud-build-api" {
  project = var.project_id
  service = "cloudbuild.googleapis.com"
}

resource "google_project_service" "cloud-error-reporting-api" {
  project = var.project_id
  service = "clouderrorreporting.googleapis.com"
}
