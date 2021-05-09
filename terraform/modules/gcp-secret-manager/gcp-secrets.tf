resource "google_secret_manager_secret" "secret-jwt-secret-key" {
  secret_id = "jwt-secret-key"

  labels = {
    tier = "backend"
  }

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "secret-user-db-password" {
  secret_id = "user-db-password"

  labels = {
    tier = "backend"
  }

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "secret-weather-db-password" {
  secret_id = "weather-db-password"

  labels = {
    tier = "backend"
  }

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}