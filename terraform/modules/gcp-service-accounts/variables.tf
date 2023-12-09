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

variable "project_id" {
  description = "The GCP project where the application will be deployed"
  type        = string
}

variable "project_number" {
  description = "The GCP project number where the application will be deployed"
  type        = string
}

variable "export_data_bucket_name" {
  description = "The name of the bucket containing the exported weather data"
  type        = string
}

variable "frontend_static_bucket_name" {
  description = "The name of the bucket containing the static files of the frontend"
  type        = string
}

variable "django-secret-key-secret-id" {
  description = "The id of the secret containing the Django secret key"
  type        = string
}

variable "frontend-db-password-secret-id" {
  description = "The id of the secret containing the frontend database password"
  type        = string
}

variable "user-db-password-secret-id" {
  description = "The id of the secret containing the user database password"
  type        = string
}

variable "weather-db-password-secret-id" {
  description = "The id of the secret containing the weather database password"
  type        = string
}

variable "jwt-secret-key-secret-id" {
  description = "The id of the secret containing the JWT secret key"
  type        = string
}
