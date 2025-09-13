# Todo DevOps Project (EKS + ArgoCD + Terraform + Helm + Prometheus)

This repo contains a simple 3-tier Todo application and full infra + CI/CD skeleton required for the DevOps take-home assignment.

## Structure
(see repo tree in submission)

## How to run
Follow `docs/SETUP.md`. Key idea:
1. Create EKS with Terraform
2. Push images to Docker Hub or use GH Actions
3. Install ArgoCD and create Argo Applications (provided)
4. ArgoCD will deploy Helm chart to cluster

## Answers (quick)
1. **Why this project?** — Demonstrates end-to-end cloud infra (EKS), GitOps (ArgoCD), IaC (Terraform + Helm), CI (GH Actions), monitoring & security basics.
2. **Security & scalability** — EKS autoscaling, multiple replicas, network policies, image scanning, secrets recommended via SealedSecrets/AWS Secrets Manager.
3. **CI/CD & monitoring** — GH Actions builds images + Trivy scans; ArgoCD syncs Helm chart automatically; Prometheus/Grafana for metrics.
4. **Biggest challenge** — Bootstrapping secure infra (IAM, secrets, network) while keeping config manageable.

