0. Architecture Design for Task Management System

This document outlines the architecture design for the Task Management System to handle high traffic, millions of tasks, and concurrent users, ensuring scalability, security, and efficiency. The design is tailored for a Windows environment with VS Code.

1. Architecture Description

Database Design

===> Primary Database: PostgreSQL will serve as the relational database, storing the tasks table with columns for id, title, description, status, and created_at. Indexes will be created on status and created_at for efficient querying.
===> Replication: A read replica will be implemented using PostgreSQL streaming replication to handle high read traffic (e.g., GET /tasks). The primary instance will handle writes, while the replica serves reads.
===> Connection Management: PgBouncer will be used as a connection pooler to manage database connections, reducing overhead and supporting concurrent users.

API Scalability

===> API Layer: FastAPI will be deployed using Uvicorn workers within Docker containers, orchestrated by Minikube (Kubernetes on Windows). This allows horizontal scaling by adding more containers based on load.
===> Load Balancing: NGINX will act as a reverse proxy and load balancer, distributing incoming requests across FastAPI instances. It will perform SSL termination and health checks to ensure only healthy instances receive traffic.
===> Scaling Strategy: Autoscaling will be configured in Minikube based on CPU/memory usage, with a minimum of 2 pods and a maximum of 10, adjustable via Horizontal Pod Autoscaler (HPA).

Authentication Setup

===> Authentication Service: Keycloak will provide role-based access control (RBAC) with predefined roles: admin (full CRUD access), user (manage own tasks), and viewer (read-only access).
===> Token-Based Authentication: Users will authenticate via OAuth2, receiving JWT tokens. FastAPI will validate these tokens using python-jose and enforce RBAC using middleware (e.g., @router.get("/tasks", dependencies=[Depends(verify_token)])).
===> Security: Tokens will be refreshed periodically, and session management will be handled by Keycloak, with logout revoking tokens.

2. Architecture Diagram (Text Form) ==>

[Users]
|
[Internet]
|
[NGINX Load Balancer]
|
[FastAPI Instances (Minikube Pods)]
| |
[Keycloak] [Redis (Caching)]
| |
[PostgreSQL Primary]----[PgBouncer]
| |
[Read Replica] [RabbitMQ (Queuing)]
| |
[Prometheus/Grafana] [Background Workers]
|
[File Logs]

Description: Users access the system via the internet, with NGINX distributing requests to scalable FastAPI pods. Keycloak handles authentication, Redis caches data, PostgreSQL (with PgBouncer) manages storage, RabbitMQ queues tasks for workers, and Prometheus/Grafana monitor performance.

3. Implementation Explanations

Caching (e.g., for Frequently Accessed Tasks)

===> Design: Redis will be used as an in-memory data store to cache frequently accessed task data, such as the results of GET /tasks. A unique cache key (e.g., tasks:skip=0:limit=10) will be generated based on query parameters.
===> Strategy:

===> Cache entries will have a 5-minute TTL to ensure data freshness.
===> On POST, PUT, and DELETE operations, the cache will be invalidated by deleting keys matching tasks:\* to reflect changes.

===> Benefits: Reduces database load by serving cached responses for read-heavy endpoints, improving latency for concurrent users.
===> Invalidation: Manual invalidation will be triggered by CRUD operations, ensuring consistency between cache and database.

Message Queuing (e.g., for Background Task Processing)

===> Design: RabbitMQ will manage a message queue, with Celery workers processing tasks asynchronously. A queue named task_processing will handle operations like sending task notifications.
===> Strategy:

===> When a task is created (POST /tasks), a message with the task ID will be sent to RabbitMQ.
===> Celery workers will dequeue and process these messages (e.g., emailing users), running in the background to avoid blocking the API.

===> Benefits: Offloads time-consuming tasks from the API, improving response times and scalability for high traffic.
===> Error Handling: Failed tasks will be retried (e.g., 3 attempts) before moving to a dead-letter queue for manual review.
