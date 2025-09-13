# SETUP.md

## Prereqs
- AWS account & credentials (AWS CLI configured)
- Terraform >= 1.2
- kubectl
- Helm
- Docker
- GitHub repo and secrets (DOCKERHUB_USERNAME, DOCKERHUB_TOKEN)

## Steps (high level)

1. Terraform:
   - `cd terraform`
   - `terraform init`
   - `terraform apply -var 'region=us-east-1'`
   - Outputs will include kubeconfig info.

2. Configure kubeconfig:
   - `aws eks update-kubeconfig --name todo-eks --region us-east-1`

3. Install ArgoCD:
   - `bash scripts/install-argocd.sh`
   - Port-forward: `kubectl port-forward svc/argocd-server -n argocd 8080:443`

4. Push Docker images:
   - Either run GitHub Actions by pushing to `main`, or build & push manually:
     - `docker build -t DOCKERHUB_USERNAME/todo-backend:latest apps/backend`
     - `docker push DOCKERHUB_USERNAME/todo-backend:latest`
     - same for frontend

5. GitOps:
   - Ensure `kubernetes/argocd/applications/*.yaml` points to your repo URL.
   - Apply ArgoCD Application manifests:
     - `kubectl apply -f kubernetes/argocd/applications/backend-app.yaml -n argocd`
     - `kubectl apply -f kubernetes/argocd/applications/frontend-app.yaml -n argocd`
   - ArgoCD will deploy the Helm chart; check `kubectl get svc` for LoadBalancer IP.

6. Monitoring:
   - Install kube-prometheus-stack via Helm and feed `monitoring/prometheus-values.yaml`.

## Security notes
- Replace DB password with Kubernetes Secret or use AWS Secrets Manager.
- Use sealed-secrets or external secrets operator for production secret management.
- CI includes Trivy scanning for images; configure severity thresholds.

