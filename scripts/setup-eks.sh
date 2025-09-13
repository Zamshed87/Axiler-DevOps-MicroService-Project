#!/usr/bin/env bash
set -euo pipefail
CLUSTER_NAME=${1:-todo-eks}
REGION=${2:-us-east-1}
echo "Assuming cluster ${CLUSTER_NAME} exists..."
aws eks update-kubeconfig --name "$CLUSTER_NAME" --region "$REGION"
echo "kubeconfig set. You can now run kubectl get nodes"
