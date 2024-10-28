resource "google_secret_manager_secret" "sa_key_secret" {
  secret_id = var.access_keys_secret_id
  replication {
    user_managed {
      replicas {
        location = var.region 
      }
    }
  }
}

resource "google_secret_manager_secret_version" "sa_key_secret_version" {
  secret      = google_secret_manager_secret.sa_key_secret.id
  secret_data = base64decode(google_service_account_key.mlflow_sa_key.private_key)
}

resource "random_password" "mlflow_db_password" {
  length  = 16
  special = false
}

resource "google_secret_manager_secret" "mlflow_db_password_secret" {
  secret_id = var.postgres_password_secret_id
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "mlflow_db_password_secret_version" {
  secret      = google_secret_manager_secret.mlflow_db_password_secret.id
  secret_data = random_password.mlflow_db_password.result
}

locals {
  postgres_db_url = "postgresql://mlflow_user:${random_password.mlflow_db_password.result}@${google_sql_database_instance.mlflow_pg_instance.public_ip_address}/mlflow_db"
}

# Create a new secret to store the full database URL
resource "google_secret_manager_secret" "mlflow_db_url_secret" {
  secret_id = var.postgres_url_secret_id
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

# Save the database URL as a secret version
resource "google_secret_manager_secret_version" "mlflow_db_url_secret_version" {
  secret      = google_secret_manager_secret.mlflow_db_url_secret.id
  secret_data = local.postgres_db_url
}

resource "google_secret_manager_secret" "mlflow_bucket_url_secret" {
  secret_id = var.bucket_secret_id
  replication {
    user_managed {
      replicas {
        location = var.region
      }
    }
  }
}

resource "google_secret_manager_secret_version" "mlflow_bucket_url_secret_version" {
  secret      = google_secret_manager_secret.mlflow_bucket_url_secret.id
  secret_data = "gs://${var.mlflow_bucket_name}/mlruns"
}
