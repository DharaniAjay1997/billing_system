# Billing System API

A production-ready **Billing Management System** built with **FastAPI**, **SQLAlchemy 2.0**, **PostgreSQL**, **Celery**, **RabbitMQ**, and **Docker**.

The application allows customers to purchase products, generates invoices, updates inventory, calculates taxes and change denominations, and sends invoice emails asynchronously.

---

# Features

- Product Management
- Customer Management
- Billing & Invoice Generation
- GST/Tax Calculation
- Purchase History
- PDF Invoice Generation
- Asynchronous Email Sending using Celery
- RabbitMQ Message Queue
- Dockerized Environment
- SQLAlchemy 2.0 ORM
- Pydantic V2 Validation
- Repository Pattern
- Service Layer Architecture
- Custom Exception Handling
- Environment Based Configuration

---

# Tech Stack

| Category | Technology |
|-----------|------------|
| Backend | FastAPI |
| Language | Python 3.12 |
| Database | PostgreSQL |
| ORM | SQLAlchemy 2.0 |
| Validation | Pydantic V2 |
| Async Tasks | Celery |
| Message Broker | RabbitMQ |
| Email Testing | MailHog |
| Database Migration | Alembic |
| Containerization | Docker & Docker Compose |
| API Docs | Swagger / OpenAPI |

---

# Project Structure

```text
app/
│
├── api/
│   └── v1/
│
├── core/
│   ├── config.py
│   ├── database.py
│   ├── base.py
│   └── exceptions.py
│
├── models/
│   ├── customer.py
│   ├── product.py
│   ├── bill.py
│   ├── bill_items.py
│   └── __init__.py
│
├── repositories/
│
├── schemas/
│
├── services/
│   ├── billing_service.py
│   └── email_service.py
│
├── task/
│   ├── celery_app.py
│   └── email_task.py
│
├── utils/
│   ├── billing_calculator.py
│   ├── denomination_calculator.py
│   └── pdf_generator.py
│
└── main.py
```

---

# Architecture

```
                Client

                   │

                   ▼

            FastAPI REST API

                   │

          Billing Service Layer

                   │

        Repository Pattern (SQLAlchemy)

                   │

             PostgreSQL Database

                   │
         ─────────────────────────

                   │

        Celery Background Worker

                   │

              RabbitMQ Queue

                   │

        Generate Invoice PDF

                   │

          Email Service (SMTP)

                   │

             Customer Email
```

---

# Billing Flow

```
Customer Purchase

      │

Validate Customer

      │

Validate Products

      │

Check Stock

      │

Calculate

    • Subtotal
    • Tax
    • Grand Total

      │

Calculate Balance

      │

Calculate Change Denominations

      │

Create Bill

      │

Create Bill Items

      │

Update Product Stock

      │

Commit Transaction

      │

Return Response

      │

Trigger Celery Task

      │

Generate PDF

      │

Send Email
```

---

# API Endpoints

## Products

| Method | Endpoint |
|----------|-------------------------|
| POST | /api/v1/products |
| GET | /api/v1/products |
| GET | /api/v1/products/{id} |
| PUT | /api/v1/products/{id} |
| DELETE | /api/v1/products/{id} |

---

## Billing

| Method | Endpoint |
|----------|-----------------------------|
| POST | /api/v1/billing |
| GET | /api/v1/billing/{id} |
| GET | /api/v1/billing/history/{email} |

---

# Invoice Calculation

The system automatically calculates

- Subtotal
- GST
- Grand Total
- Balance
- Change Denominations

Example

```
Product A

Price : ₹100
Qty : 2
Tax : 18%

Subtotal = 200

GST = 36

Grand Total = 236
```

---

# Change Denomination

Example

```
Grand Total

₹820

Cash Paid

₹1000

Balance

₹180

Denominations

100 x 1

50 x 1

20 x 1

10 x 1
```

---

# Email Workflow

```
Bill Created

      │

Celery Task Created

      │

RabbitMQ Queue

      │

Worker Picks Task

      │

Fetch Bill

      │

Generate PDF

      │

Send Email

      │

Delete Temporary PDF
```

---

# Environment Variables

Create a `.env` file.

```env
APP_NAME=Billing System

DATABASE_URL=postgresql://postgres:postgres@db:5432/billing_db

SMTP_SERVER=mailhog
SMTP_PORT=1025
SMTP_USERNAME=
SMTP_PASSWORD=
```

---

# Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

Stop

```bash
docker compose down
```

---

# Running Alembic

Create Migration

```bash
alembic revision --autogenerate -m "Initial migration"
```

Upgrade

```bash
alembic upgrade head
```

---

# Celery

Start Worker

```bash
celery -A app.task.celery_app.celery worker --loglevel=info
```

Inspect Registered Tasks

```bash
celery -A app.task.celery_app.celery inspect registered
```

Worker Status

```bash
celery -A app.task.celery_app.celery status
```

---

# MailHog

SMTP

```
Host : mailhog

Port : 1025
```

Web UI

```
http://localhost:8025
```

---

# Swagger

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---

# Error Handling

The application uses centralized exception handling.

Examples

```
404 Resource Not Found

400 Validation Error

500 Internal Server Error
```

---

# Design Patterns Used

- Repository Pattern
- Service Layer Pattern
- Dependency Injection
- Factory Pattern (Session)
- Background Worker Pattern
- DTO Pattern (Pydantic Schemas)

---

# Future Improvements

- JWT Authentication
- Role Based Authorization
- Redis Caching
- API Rate Limiting
- Payment Gateway Integration
- Kubernetes Deployment
- CI/CD Pipeline
- Unit Testing
- Integration Testing
- Prometheus Metrics
- Grafana Dashboard
- OpenTelemetry Tracing
- Kafka Event Streaming
- S3 Invoice Storage

---

# Technologies Demonstrated

- FastAPI
- SQLAlchemy 2.0
- PostgreSQL
- Alembic
- Celery
- RabbitMQ
- MailHog
- Docker
- Repository Pattern
- Dependency Injection
- Pydantic V2
- Background Processing
- PDF Generation
- SMTP Email
- Inventory Management
- Clean Architecture

---

# Author

Built as a backend engineering assessment demonstrating production-ready backend development using Python and FastAPI.
