# shopping-system-k8s

A Kubernetes-based shopping system composed of Python microservices, designed to demonstrate a scalable architecture using KEDA for event-driven autoscaling.

## Overview

This project consists of two main microservices:

- **Web Server**: A frontend-facing service.
- **Management API**: An internal API for managing system resources, integrating with Kafka and MongoDB.

The infrastructure is managed via Helm charts and utilizes KEDA (Kubernetes Event-driven Autoscaling) to scale the services based on demand.

## Prerequisites

Before running this project, ensure you have the following installed:

- [Kubernetes](https://kubernetes.io/) cluster (e.g., Minikube, Kind, Docker Desktop, or a remote cluster)
- [Helm](https://helm.sh/) (v3+)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) configured to talk to your cluster

## Project Structure

```text
.
├── apps/                       # Source code for microservices
│   ├── management-api/         # Python FastAPI service (Kafka consumers, MongoDB)
│   └── web-server/             # Python web server
├── helm-chart/                 # Kubernetes deployment configurations
│   ├── setup-env.sh            # One-click setup script
│   └── shopping-system/        # Main Helm chart for the application
└── README.md
```

## Getting Started

### Quick Setup

A setup script is provided to install necessary dependencies (like KEDA) and deploy the application.

1. Navigate to the `helm-chart` directory:

   ```bash
   cd helm-chart
   ```

2. Run the setup script:

   ```bash
   ./setup-env.sh
   ```

   This script will:
   - Install KEDA into the `keda` namespace.
   - Build Helm dependencies.
   - Deploy the `shopping-system` chart into the `shopping-system` namespace.

### Manual Deployment

If you prefer to deploy manually:

1. **Install KEDA**:

   ```bash
   helm repo add kedacore https://kedacore.github.io/charts
   helm repo update
   helm upgrade --install keda kedacore/keda --namespace keda --create-namespace --wait
   ```

2. **Deploy Application**:

   ```bash
   cd helm-chart/shopping-system
   helm dependency build .
   helm upgrade --install my-assignment . --namespace shopping-system --create-namespace --wait
   ```

## Services

- **Web Server**: Handles incoming HTTP requests from users.
- **Management API**: Processes background tasks and manages data persistence using MongoDB and Kafka.

## Troubleshooting

- Check the status of the pods:

  ```bash
  kubectl get pods -n shopping-system
  ```

- View logs for a specific service:

  ```bash
  kubectl logs -f <pod-name> -n shopping-system
  ```
