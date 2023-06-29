module "llm_gke_cluster" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/gke-cluster-autopilot"
  project_id = var.project_id
  name       = "${var.name}-llm"
  location   = var.location
  vpc_config = {
    network    = module.vpc.self_link
    subnetwork = module.vpc.subnet_self_links["europe-west1/production"]
    secondary_range_names = {
      pods     = "pods"
      services = "services"
    }
    master_authorized_ranges = {
      internal-vms = "10.0.0.0/8"
    }
    master_ipv4_cidr_block = "192.168.0.0/28"
  }
  private_cluster_config = {
    enable_private_endpoint = true
    master_global_access    = false
  }
  enable_addons = {
    horizontal_pod_autoscaling = true
    http_load_balancing        = true
    cloudrun                   = true
  }
}

module "vpc" {
  source     = "github.com/GoogleCloudPlatform/cloud-foundation-fabric//modules/net-vpc"
  project_id = var.project_id
  name       = var.name
  subnets = [
    {
      ip_cidr_range = "10.0.0.0/24"
      name          = "default"
      region        = var.location
      secondary_ip_ranges = {
        pods     = "172.16.0.0/20"
        services = "192.168.0.0/24"
      }
    },
  ]
}
