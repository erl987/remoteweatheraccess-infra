resource "google_secret_manager_secret_version" "secret-version-jwt-secret-key" {
  secret = google_secret_manager_secret.secret-jwt-secret-key.id
  secret_data = random_password.random-jwt-secret-key.result
}

resource "google_secret_manager_secret_version" "secret-version-user-db-password" {
  secret = google_secret_manager_secret.secret-user-db-password.id
  secret_data = var.user-db-password
}

resource "google_secret_manager_secret_version" "secret-version-weather-db-password" {
  secret = google_secret_manager_secret.secret-weather-db-password.id
  secret_data = var.weatherdata-db-password

}