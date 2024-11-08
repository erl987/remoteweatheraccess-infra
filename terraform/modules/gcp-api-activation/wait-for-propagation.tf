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

# the time to wait (in seconds) in order to have the API activation propagate in the GCP - this is a workaround
locals {
  wait-time = 60
}

resource "null_resource" "resource-to-wait-on" {
  provisioner "local-exec" {
    command = "sleep ${local.wait-time}"
  }
  depends_on = [
    google_project_service.secret-manager-api,
    google_project_service.cloud-run-api,
    google_project_service.cloud-sql-admin-api,
    google_project_service.cloud-storage-api,
    google_project_service.app-engine-api,
    google_project_service.cloud-scheduler-api,
    google_project_service.cloud-build-api,
    google_project_service.cloud-error-reporting-api
  ]
}