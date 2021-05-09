resource "google_service_account" "frontend-service-account" {
  account_id = "weather-frontend"
  display_name = "Weather website frontend"
}

resource "google_service_account" "backend-service-account" {
  account_id = "weather-backend"
  display_name = "Weather website backend"
}