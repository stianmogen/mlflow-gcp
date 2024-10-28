# Define the Cloud Run service for the MLflow server
resource "google_cloud_run_service" "mlflow_server" {
  name     = "mlflow-server"
  location = var.region

  template {
    spec {
      containers {
        name = "mlflow-server"
        image = "${var.region}-docker.pkg.dev/${var.project_id}/${var.artifact_repo_name}/mlflow-server:latest"
        resources {
          limits = {
            cpu = "1000m"
            memory = "1Gi"
          }
        }
      }
      timeout_seconds = 300
    }
  }
  traffic {
    percent         = 100
    latest_revision = true
  }
}
