# Usage Insights SaaS Platform

A multi-tenant SaaS feature designed to track user events, calculate daily aggregates, and notify customers when usage crosses predefined thresholds. 

Built as a Tech Lead take-home assignment, demonstrating clean architecture, separation of concerns, and scalable aggregation strategies.

---

## 🏗 System Architecture
Please see the [`architecture.md`](./architecture.md) file in this repository for a comprehensive breakdown of the system design, data flow, and scaling strategy.

---

## 🚀 Quick Start (Local Setup)

We've provided a `Makefile` to make local setup and running as frictionless as possible.

### 1. Install Dependencies & Setup DB
Run this command once to install both Python and Node dependencies, and to migrate the SQLite database:
```bash
make setup
```

### 2. Start the Backend (Terminal 1)
```bash
make start-backend
```
*The Django REST API will be available at `http://localhost:8000`*

### 3. Start the Frontend (Terminal 2)
```bash
make start-frontend
```
*The React Dashboard will be available at `http://localhost:5173`*

---

## 🧪 Testing

The backend includes a comprehensive automated test suite testing the ingestion, aggregation, and threshold logic using `pytest` and `django.db`.

To run the automated tests:
```bash
make test
```

---

## 💻 Tech Stack
- **Backend**: Django 5.0, Django REST Framework, SQLite (Swappable to PostgreSQL), Pytest
- **Frontend**: React (Vite), Axios, Recharts
- **Architecture**: Service Layer Pattern

---

## 🔌 API Endpoints

### `POST /api/events/`
Ingests a raw usage event.

**Payload:**
```json
{
  "account_id": 1,
  "user_id": 1,
  "team_id": 1,
  "event_type": "click",
  "feature_name": "dashboard",
  "metadata": {"button": "save"}
}
```

### `GET /api/usage/?account_id=1`
Fetches pre-aggregated usage data for the dashboard charts. Returns Daily, Feature, and Team usage arrays dynamically derived from the `DailyUsageAggregate` table.

### `POST /api/thresholds/`
Create or update threshold limits.

**Payload:**
```json
{
  "account_id": 1,
  "feature_name": "dashboard",
  "limit": 100
}
```

### `GET /api/thresholds/?account_id=1`
Fetches the active threshold configurations for a given account. Returns a list of configured feature thresholds.
