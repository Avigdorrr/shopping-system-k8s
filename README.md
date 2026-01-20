# shopping-system-k8s

A Kubernetes-based shopping system composed of Python microservices, designed to demonstrate a scalable architecture using KEDA for event-driven autoscaling.

## Overview

This project consists of two main microservices:

- **Web Server**: A frontend-facing service that produces events to Kafka.
- **Management API**: An internal API for managing system resources, integrating with Kafka and MongoDB.

The infrastructure is managed via Helm charts and utilizes KEDA (Kubernetes Event-driven Autoscaling) to scale the services based on demand.

## Requirements

Before running this project, ensure you have the following installed:

- [Kubernetes](https://kubernetes.io/) cluster (e.g., Minikube, Kind, Docker Desktop, or a remote cluster)
- [Helm](https://helm.sh/) (v3+)
- [kubectl](https://kubernetes.io/docs/tasks/tools/) configured to talk to your cluster

## Helm Chart Deployment

This project uses a [Helm](https://helm.sh/) chart to manage the entire application stack. The chart is designed to simplify deployment by:

1. **Managing Dependencies**: It automatically installs and configures required infrastructure services:
    - **Kafka**: For event streaming between services.
    - **MongoDB**: For data persistence.
2. **Configuration Management**: It centrally handles configuration (ports, topic, autoscaling) through a single `values.yaml` file.
3. **Service Discovery**: It automatically injects the correct connection strings (Kafka bootstrap servers, MongoDB URIs) into the applications, so they can talk to each other without manual setup.

## Project Structure

```text
.
├── apps/                       # Source code for microservices
│   ├── management-api/         # Python FastAPI service (Kafka consumer, MongoDB)
│   └── web-server/             # Python FastAPI service (Kafka producer)
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

## CI/CD Pipeline

The project includes a comprehensive CI/CD pipeline using **GitHub Actions**.

### Workflow

1. **Testing**:
    - On every push to `main`, the pipeline runs simple health checks (`pytest`) for both `management-api` and `web-server`.
    - Tests are run using **Python 3.14** to ensure compatibility with the deployment environment.

2. **Build & Push**:
    - If tests pass, the pipeline builds Docker images for both services.
    - Images are built for multiple platforms (**linux/amd64** and **linux/arm64**).
        - **Why?** This ensures native performance and compatibility with **Apple Silicon (M1/M2/M3)** chips, which is the hardware used to develop and test this project.
    - Images are pushed to Docker Hub with two tags:
        - `latest`
        - `sha-<git-short-sha>`

3. **Deployment Instructions**:
    - The development environment for this project is **Minikube**.
    - Since the GitHub Actions runner cannot access the local Minikube cluster, the pipeline skips auto-deployment.
    - Instead, it outputs the exact **Helm** commands needed to deploy the specific version built by the CI.
    - You can copy these commands from the GitHub Actions logs to deploy the newly built images to your local cluster.

## Testing the System

Once the system is running, you can interact with the services using **curl**, **Postman**, or **Swagger UI**.

### Accessing the Services

To access the services locally, you can use `kubectl port-forward`.

> **Note**: The service names depend on the Helm release name you used. If you followed the instructions and used `my-assignment`, the names will be as follows. If you used a different name, check `kubectl get svc -n shopping-system`.

```bash
# Web Server (Port 8081)
kubectl port-forward svc/my-assignment-shopping-system-web-server 8081:8081 -n shopping-system

# Management API (Port 8080)
kubectl port-forward svc/my-assignment-shopping-system-management-api 8080:8080 -n shopping-system
```

### Swagger UI

Both services provide interactive API documentation via Swagger UI, available at `/docs`:

- **Web Server**: [http://localhost:8081/docs](http://localhost:8081/docs)
- **Management API**: [http://localhost:8080/docs](http://localhost:8080/docs)

### API Endpoints

#### 1. Simulate a Purchase

**Endpoint**: `POST /api/v1/buy` (Web Server)

This endpoint accepts a purchase request and publishes an event to Kafka.

**Request Body**:

```json
{
  "username": "user1",
  "userid": "123",
  "price": 50.0
}
```

**Response Example** (`202 Accepted`):

```json
{
  "status": "success",
  "message": "Purchase recorded",
  "data": {
    "username": "user1",
    "userid": "123",
    "price": 50.0,
    "timestamp": 1705663200.123456
  }
}
```

**curl Example**:

```bash
curl -X POST "http://localhost:8081/api/v1/buy" \
     -H "Content-Type: application/json" \
     -d '{"username": "user1", "userid": "123", "price": 50.0}'
```

#### 2. Get User Purchase History (via Web Server)

**Endpoint**: `GET /api/v1/getAllUserBuys/{userid}` (Web Server)

This endpoint proxies the request to the Management API to retrieve the user's purchase history.

**Response Example** (`200 OK`):

```json
[
  {
    "userid": "123",
    "username": "user1",
    "price": 50.0,
    "timestamp": 1705663200.123456
  }
]
```

**curl Example**:

```bash
curl -X GET "http://localhost:8081/api/v1/getAllUserBuys/123"
```

#### 3. Get User Purchase History (Directly from Management API)

**Endpoint**: `GET /api/v1/purchases/{userid}` (Management API)

You can also query the Management API directly if you have port-forwarded it.

**Response Example** (`200 OK`):

```json
[
  {
    "userid": "123",
    "username": "user1",
    "price": 50.0,
    "timestamp": 1705663200.123456
  }
]
```

**curl Example**:

```bash
curl -X GET "http://localhost:8080/api/v1/purchases/123"
```

## Troubleshooting

- Check the status of the pods:

  ```bash
  kubectl get pods -n shopping-system
  ```

- View logs for a specific service:

  ```bash
  kubectl logs -f <pod-name> -n shopping-system
  ```
