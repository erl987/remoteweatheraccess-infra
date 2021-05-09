# the time to wait (in seconds) in order to have the API activation propagate in the GCP - this is a workaround
locals {
  wait-time = 60
}

resource "null_resource" "resource-to-wait-on" {
  provisioner "local-exec" {
    command = "sleep ${local.wait-time}"
  }
  depends_on = [
    google_project_service.secret-manager-api,
    google_project_service.container-registry-api,
    google_project_service.cloud-run-api,
    google_project_service.cloud-sql-admin-api]
}