resource "google_project_iam_binding" "service-account-secret-accessor-role" {
  project = var.project_id
  role = "roles/secretmanager.secretAccessor"

  members = [
    "serviceAccount:${google_service_account.frontend-service-account.email}",
    "serviceAccount:${google_service_account.backend-service-account.email}"]
}

resource "google_project_iam_binding" "service-account-sql-client-role" {
  project = var.project_id
  role = "roles/cloudsql.client"

  members = [
    "serviceAccount:${google_service_account.backend-service-account.email}"]
}
