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

output "user-db-password" {
  description = "The password for the `userdb` user of the database"
  value       = random_password.random-user-db-password.result
}

output "weatherdata-db-password" {
  description = "The password for the `weatherdatadb` user of the database"
  value       = random_password.random-weatherdata-db-password.result
}

output "frontend-db-password" {
  description = "The password for the `frontend_db` user of the database"
  value       = random_password.random-frontend-db-password.result
}