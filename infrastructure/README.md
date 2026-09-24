# infrastructure

**Deployment.** Two targets, both defined as code. The blueprint files carry their reasoning in comments.

| | |
|---|---|
| `preprod/` | a managed-host blueprint — the public demo, 0.5 CPU and 512 MB, and a static UI that rewrites /api to keep the browser same-origin |
| `production/` | Terraform for the AWS topology: ALB, ECS Fargate, RDS in private subnets, S3 to SQS ingestion, Secrets Manager |
| `shared/` | the container registry and certificate both environments use |

_Implementations are private. This file lists what lives here and what it is responsible for._
