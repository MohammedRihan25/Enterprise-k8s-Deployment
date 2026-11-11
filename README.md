# Enterprise-Grade Kubernetes Deployment

End-to-end cloud-native DevOps portfolio project demonstrating containerization, Infrastructure as Code (Terraform), Kubernetes orchestration with auto-scaling (HPA), HTTPS Ingress, and observability (Prometheus & Grafana).

## Architecture Overview
1. **Dockerize the API:** `weather-api` packaged into a production multi-stage Docker image.
2. **Cluster via Terraform:** AWS VPC, subnets, IAM, and EKS provisioned via code.
3. **Deploy + Production:** Kubernetes deployment with 2 base pods scaling to 4 via HPA, secured with HTTPS Ingress, and monitored with Prometheus & Grafana.
