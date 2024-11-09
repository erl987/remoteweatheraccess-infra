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

resource "google_storage_bucket" "weather-export-data-bucket" {
  name     = format("weather-export-data-%s", tostring(random_integer.random-bucket-id.result))
  location = var.region
  project  = var.project_id

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "frontend-static-bucket" {
  name     = format("frontend-static-%s", tostring(random_integer.random-bucket-id.result))
  location = var.region
  project  = var.project_id

  uniform_bucket_level_access = true
}

resource "google_storage_bucket" "cloud-build-bucket" {
  name     = format("cloud-build-%s", tostring(random_integer.random-bucket-id.result))
  location = var.region
  project  = var.project_id

  uniform_bucket_level_access = true

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 1
    }
  }
}
