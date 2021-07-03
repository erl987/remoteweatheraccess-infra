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

variable "region" {
  description = "The GCP region where the application will be deployed"
  type = string
}

variable "database_version" {
  description = "The Postgres database version for the weather database. The choice depends on the availability in GCP"
  type = string
}

variable "sql_backup_region" {
  description = "GCP region (or multi-region) for the database backup"
  type = string
}

variable "database_tier" {
  description = "The machine type used for the database. Must be a GCP-machine type available for Cloud SQL"
  type = string
}
