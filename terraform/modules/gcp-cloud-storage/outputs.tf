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

output "export-data-bucket-name" {
  description = "The name of the bucket containing the exported weather data"
  value       = google_storage_bucket.weather-export-data-bucket.name
}

output "frontend-static-bucket-name" {
  description = "The name of the bucket containing the static files of the frontend"
  value       = google_storage_bucket.frontend-static-bucket.name
}
