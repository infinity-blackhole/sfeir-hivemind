module "service_account" {
  source  = "terraform-google-modules/service-accounts/google"
  version = "~> 4.2"

  project_id   = var.project_id
  names        = [var.name]
  display_name = "${var.display_name} service account"
  project_roles = [
    "${var.project_id}=>roles/aiplatform.user",
    "${var.project_id}=>roles/datastore.user"
  ]
}
