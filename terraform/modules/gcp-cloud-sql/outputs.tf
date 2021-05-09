# output variable definitions

output "user-db-password" {
  description = "The password for the `userdb` user of the database"
  value = random_password.random-user-db-password.result
}

output "weatherdata-db-password" {
  description = "The password for the `weatherdatadb` user of the database"
  value = random_password.random-weatherdata-db-password.result
}