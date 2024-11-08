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

resource "google_service_account" "frontend-service-account" {
  account_id   = "weather-frontend"
  display_name = "Weather website frontend"
}

resource "google_service_account" "backend-service-account" {
  account_id   = "weather-backend"
  display_name = "Weather website backend"
}

resource "google_service_account" "exporter-service-account" {
  account_id   = "weather-exporter"
  display_name = "Weather data file exporter"
}