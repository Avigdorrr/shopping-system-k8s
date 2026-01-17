#!/bin/bash

echo "Starting Setup..."

# 1. Install KEDA (Infrastructure Layer)
echo "Installing KEDA..."
helm repo add kedacore https://kedacore.github.io/charts
helm repo update
helm upgrade --install keda kedacore/keda \
  --namespace keda \
  --create-namespace \
  --wait # Waits for KEDA to be ready before moving on

# 2. Install The Application (Umbrella Chart)
echo "Installing Application Stack..."
# Assuming you are in the folder containing the umbrella chart
helm dependency build . 
helm upgrade --install my-assignment . \
  --namespace shopping-system \
  --create-namespace \
  --wait

echo "Setup Complete! Check the pods with: kubectl get pods"