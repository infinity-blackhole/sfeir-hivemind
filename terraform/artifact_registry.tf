module "docker_artifact_registry" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/artifact-registry"
  project_id = var.project_id
  location   = var.location
  labels     = var.labels
  format     = "DOCKER"
  id         = var.name
  iam = {
    "roles/artifactregistry.reader" = [module.service_account.iam_email]
  }
}
