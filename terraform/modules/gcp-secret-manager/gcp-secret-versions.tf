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

resource "google_secret_manager_secret_version" "secret-version-jwt-secret-key" {
  secret = google_secret_manager_secret.secret-jwt-secret-key.id
  secret_data = random_password.random-jwt-secret-key.result
}

resource "google_secret_manager_secret_version" "secret-version-user-db-password" {
  secret = google_secret_manager_secret.secret-user-db-password.id
  secret_data = var.user-db-password
}

resource "google_secret_manager_secret_version" "secret-version-weather-db-password" {
  secret = google_secret_manager_secret.secret-weather-db-password.id
  secret_data = var.weatherdata-db-password

}