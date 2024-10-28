resource "google_storage_bucket" "mlflow_bucket" {
  name          = var.mlflow_bucket_name
  location      = var.region
  force_destroy = true
}

resource "google_storage_bucket" "terraform_state" {
  name          = var.tf_bucket_name
  location      = var.region
  force_destroy = true   
}