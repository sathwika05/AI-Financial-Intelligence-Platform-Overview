# infrastructure/production

**AWS topology (Terraform).** ALB to ECS Fargate — an API task and an ingestion worker sharing one image — with RDS in private subnets, S3 to SQS ingestion and Secrets Manager.

| | |
|---|---|
| `network.tf` | VPC, subnets, the load balancer |
| `compute.tf` | the cluster, task definitions and services |
| `database.tf` | RDS and its parameter group |
| `storage.tf` | buckets and queues |
| `variables.tf / outputs.tf / providers.tf` | inputs, outputs, provider pinning |

_Implementations are private. This file lists what lives here and what it is responsible for._
