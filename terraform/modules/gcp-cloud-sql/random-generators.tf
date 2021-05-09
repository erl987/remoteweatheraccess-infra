resource "random_password" "random-user-db-password" {
  length = 20
  special = true
}

resource "random_password" "random-weatherdata-db-password" {
  length = 20
  special = true
}

resource "random_integer" "random-database-id" {
  min = 100000
  max = 999999
}