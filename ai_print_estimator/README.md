# AI Print Estimator

Production-ready AI-powered print estimation and order intake system.

## Features
- Accepts unstructured print orders
- AI-based spec extraction
- Deterministic pricing engine
- Validation & feasibility checks
- Workflow orchestration using n8n

## Tech Stack
FastAPI | PostgreSQL | OpenAI | n8n | Docker

## Setup

```bash
docker-compose up --build

API available at:
http://localhost:8000/docs

Example Request

POST /orders/text

{
  "message": "500 A4 brochures, 170 GSM, matte finish, delivery in 3 days"
}