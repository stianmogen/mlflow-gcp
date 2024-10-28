
data "google_secret_manager_secret_version" "db_password_secret" {
  secret = var.postgres_password_secret_id
}

# Create a Cloud SQL instance with PostgreSQL
resource "google_sql_database_instance" "mlflow_pg_instance" {
  name             = var.mlflow_db_instance_name
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier          = "db-f1-micro"
    disk_type     = "PD_HDD"
    disk_size     = 10  # Size in GB
    backup_configuration {
      enabled = false
    }

    ip_configuration {
      ipv4_enabled = true  # Enable IPv4
      authorized_networks {
        value = "0.0.0.0/0"  # Replace with your trusted networks
      }
    }
  }
}

# Create the MLFlow database within the Cloud SQL instance
resource "google_sql_database" "mlflow_db" {
  name     = var.mlflow_db_name
  instance = google_sql_database_instance.mlflow_pg_instance.name
}

# Create a database user for MLFlow, using the password from Secret Manager
resource "google_sql_user" "mlflow_user" {
  name     = var.mlflow_db_user_name
  instance = google_sql_database_instance.mlflow_pg_instance.name
  password = data.google_secret_manager_secret_version.db_password_secret.secret_data
}