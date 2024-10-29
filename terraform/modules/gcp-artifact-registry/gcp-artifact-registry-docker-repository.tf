resource "google_artifact_registry_repository" "web-app-docker-repo" {
  location               = var.region
  project                = var.project_id
  repository_id          = "webapp"
  description            = "The web app containers"
  format                 = "DOCKER"
  cleanup_policy_dry_run = false
  cleanup_policies {
    id     = "keep-latest"
    action = "KEEP"
    most_recent_versions {
      keep_count = 5
    }
  }
  cleanup_policies {
    id     = "delete"
    action = "DELETE"
    condition {
      tag_state  = "ANY"
      older_than = "3600s"
    }
  }
}
