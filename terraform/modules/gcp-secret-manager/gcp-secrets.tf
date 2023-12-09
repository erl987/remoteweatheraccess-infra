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

resource "google_secret_manager_secret" "secret-frontend-db-password" {
  secret_id = "frontend-db-password"

  labels = {
    tier = "frontend"
  }

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret" "secret-django-secret-key" {
  secret_id = "django-secret-key"

  labels = {
    tier = "frontend"
  }

  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}
