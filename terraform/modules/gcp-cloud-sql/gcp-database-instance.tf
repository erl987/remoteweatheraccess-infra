resource "google_sql_database_instance" "weather-database-instance" {
  name = format("weatherdata-db-%s", tostring(random_integer.random-database-id.result))
  database_version = var.database_version
  region = var.region

  settings {
    tier = var.database_tier

    backup_configuration {
      enabled = true
      start_time = "23:00"
      point_in_time_recovery_enabled = true
      location = var.sql_backup_region

      //noinspection HCLUnknownBlockType
      backup_retention_settings {
        retained_backups = 7
        retention_unit = "COUNT"
      }
    }

    maintenance_window {
      day = 7
      hour = 0
      update_track = "stable"
    }
  }

  lifecycle {
    prevent_destroy = true
  }
}
