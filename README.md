# shopping-system-k8s

A Kubernetes-based shopping system composed of Python microservices, designed to demonstrate a scalable architecture using KEDA for event-driven autoscaling.

## Overview

This project consists of two main microservices:

- **Web Server**: A frontend-facing service that produces events to Kafka.
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
│   ├── management-api/         # Python FastAPI service (Kafka consumer, MongoDB)
│   └── web-server/             # Python web server (Kafka producer)
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

- **Web Server**: Handles incoming HTTP requests from users and produces events to Kafka.
- **Management API**: Processes background tasks and manages data persistence using MongoDB and Kafka.

## Autoscaling

The system uses [KEDA](https://keda.sh/) (Kubernetes Event-driven Autoscaling) to scale services dynamically based on workload and metrics:

- **Web Server**: Scales based on **CPU utilization**.
  - **Why?** Since this is a frontend-facing service, high traffic correlates with increased CPU usage. Scaling on CPU ensures the service remains responsive under load.

- **Management API**: Scales based on **Kafka Consumer Lag**.
  - **Why?** This service processes background events. If the producer (Web Server) generates events faster than the consumer can process them, the "lag" (pending messages) increases. KEDA detects this and adds more pods to drain the queue faster, ensuring eventual consistency.

## Troubleshooting

- Check the status of the pods:

  ```bash
  kubectl get pods -n shopping-system
  ```

- View logs for a specific service:

  ```bash
  kubectl logs -f <pod-name> -n shopping-system
  ```
