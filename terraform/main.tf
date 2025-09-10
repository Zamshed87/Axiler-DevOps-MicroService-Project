provider "aws" {
  region = var.aws_region
}

# EKS module example (uses community module as placeholder)
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = var.cluster_name
  cluster_version = "1.26"
  subnets         = var.subnets
  vpc_id          = var.vpc_id
  node_groups = {
    default = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1
      instance_type    = "t3.medium"
    }
  }
}

output "cluster_name" {
  value = module.eks.cluster_id
}
