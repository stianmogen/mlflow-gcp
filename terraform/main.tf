provider "google" {
  project = var.project_id
  region  = var.region
}

terraform {
  backend "gcs" {
    bucket  = "terraform-state-${var.project_id}"
    prefix  = "terraform/state" 
  }
}
