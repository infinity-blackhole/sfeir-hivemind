module "docker_artifact_registry" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/artifact-registry"
  project_id = var.project_id
  name       = var.name
  location   = var.location
  labels     = var.labels
  format = {
    docker = {
      immutable_tags = true
    }
  }
  iam = {
    "roles/artifactregistry.reader" = [module.service_account.iam_email]
  }
}
