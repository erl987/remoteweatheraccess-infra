resource "google_sql_user" "users-database-user" {
  instance = google_sql_database_instance.weather-database-instance.name
  name = "userdb"
  password = random_password.random-user-db-password.result
}

resource "google_sql_user" "weather-data-database-user" {
  instance = google_sql_database_instance.weather-database-instance.name
  name = "weatherdatadb"
  password = random_password.random-weatherdata-db-password.result
}