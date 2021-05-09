# input variable definitions

variable "region" {
  description = "The GCP region where the application will be deployed"
  type = string
}

variable "user-db-password" {
  description = "The password for the `userdb` user of the database"
  type = string
}

variable "weatherdata-db-password" {
  description = "The password for the `weatherdatadb` user of the database"
  type = string
}