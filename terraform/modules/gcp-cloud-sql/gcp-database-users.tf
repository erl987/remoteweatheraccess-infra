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

resource "google_sql_user" "users-database-user" {
  instance = google_sql_database_instance.weather-database-instance.name
  name     = "userdb"
  password = random_password.random-user-db-password.result

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_sql_user" "weather-data-database-user" {
  instance = google_sql_database_instance.weather-database-instance.name
  name     = "weatherdatadb"
  password = random_password.random-weatherdata-db-password.result

  lifecycle {
    prevent_destroy = true
  }
}

resource "google_sql_user" "frontend-database-user" {
  instance = google_sql_database_instance.weather-database-instance.name
  name     = "frontend_db"
  password = random_password.random-frontend-db-password.result

  lifecycle {
    prevent_destroy = true
  }
}