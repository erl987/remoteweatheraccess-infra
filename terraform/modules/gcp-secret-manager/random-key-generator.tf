resource "random_password" "random-jwt-secret-key" {
  length = 232
  special = true
}