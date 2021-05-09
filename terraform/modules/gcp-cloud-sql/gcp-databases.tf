resource "google_sql_database" "users-database" {
  name = "users"
  instance = google_sql_database_instance.weather-database-instance.name
}

resource "google_sql_database" "weather-data-database" {
  name = "weatherdata"
  instance = google_sql_database_instance.weather-database-instance.name
}