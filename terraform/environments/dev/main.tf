terraform {
  backend "local" {}
}

module "dev" {
  source = "../../"

  aws_region   = "us-east-1"
  cluster_name = "axiler-eks-dev"
}
