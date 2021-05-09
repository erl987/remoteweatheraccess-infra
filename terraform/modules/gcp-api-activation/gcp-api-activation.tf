resource "google_project_service" "secret-manager-api" {
  project = var.project_id
  service = "secretmanager.googleapis.com"
}

resource "google_project_service" "container-registry-api" {
  project = var.project_id
  service = "containerregistry.googleapis.com"
}

resource "google_project_service" "cloud-run-api" {
  project = var.project_id
  service = "run.googleapis.com"
}

resource "google_project_service" "cloud-sql-admin-api" {
  project = var.project_id
  service = "sqladmin.googleapis.com"
}
