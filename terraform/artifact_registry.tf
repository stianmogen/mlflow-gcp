resource "google_artifact_registry_repository" "artifact_repo" {
  repository_id = var.artifact_repo_name
  format        = "DOCKER"
  location      = var.region
  description   = "Docker repository for mlflow server"
}
