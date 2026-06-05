# IncidentFlow

A microservices-based incident management system built with FastAPI, Kafka, PostgreSQL, and Redis. When an incident is created via the API, it is persisted to PostgreSQL and an event is published to Kafka. A background worker consumes the event, processes the incident, and updates its status in Redis.

## Architecture

```
┌────────────┐       ┌─────────┐       ┌────────────┐       ┌───────┐
│  FastAPI   │──────▶│  Kafka  │──────▶│   Worker   │──────▶│ Redis │
│   (API)    │       │         │       │ (Consumer) │       │       │
└─────┬──────┘       └─────────┘       └────────────┘       └───────┘
      │
      ▼
┌────────────┐
│ PostgreSQL │
└────────────┘
```

## Services

| Service    | Description                              | Port  |
|------------|------------------------------------------|-------|
| api        | FastAPI REST API                          | 8000  |
| db         | PostgreSQL 15 database                    | 5432  |
| kafka      | Confluent Kafka broker                    | 9092  |
| zookeeper  | Kafka coordination service                | 2181  |
| redis      | Redis for processed status tracking       | 6379  |
| worker     | Kafka consumer that processes incidents   | —     |
| kafka-ui   | Web UI for inspecting Kafka topics        | 8080  |

## Getting Started

### Prerequisites

- Docker & Docker Compose

### Run

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.  
Kafka UI will be available at `http://localhost:8080`.

### Environment Variables

Create a `.env` file in the project root with:

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/incidentflow
```

## API Endpoints

### Health Check

```
GET /health
```

### Create Incident

```
POST /incidents
```

**Body:**

```json
{
  "service_name": "auth-service",
  "severity": "high",
  "message": "Latency spike detected"
}
```

### List Incidents

```
GET /incidents
```

### Get Incident

```
GET /incidents/{incident_id}
```

### Get Incident Processing Status

```
GET /incidents/{incident_id}/status
```

Returns the processing status from Redis (`processed` or `not_processed`).

## How It Works

1. A `POST /incidents` request creates an incident in PostgreSQL.
2. The API publishes an `incident.created` event to Kafka.
3. The worker consumes the event, simulates processing (5s delay), and sets the status to `processed` in Redis.
4. The `/incidents/{id}/status` endpoint reads the processing result from Redis.

## Tech Stack

- **API:** FastAPI, SQLAlchemy, Pydantic
- **Broker:** Apache Kafka (Confluent)
- **Database:** PostgreSQL 15
- **Cache/State:** Redis 7
- **Worker:** kafka-python consumer
- **Containerization:** Docker Compose