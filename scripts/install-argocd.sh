#!/usr/bin/env bash
set -euo pipefail
kubectl create namespace argocd || true
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
echo "Waiting for argocd server..."
kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=180s || true
echo "ArgoCD installed in namespace argocd. To port-forward run:"
echo "kubectl port-forward svc/argocd-server -n argocd 8080:443"
