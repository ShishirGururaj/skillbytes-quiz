# SkillBytes Quiz Application

A WhatsApp-style quiz application built with **React, FastAPI, and MongoDB**.

## Tech Stack

* React + TypeScript + Vite
* FastAPI + Python
* MongoDB
* PyMongo
* pytest

## Architecture

```text
React Frontend
      |
      v
FastAPI REST API
      |
      v
MongoDB
```

Backend responsibilities are separated into **routes, schemas, services, database access, and configuration**.

### Application Flow

```text
Login → Exam → Subject → Chapter → Quiz → Result
```

Users answer multiple-choice questions sequentially and cannot revisit previous questions.

## Analytics

Question-attempt events are stored in MongoDB and used as the source of truth for:

* **Learning Velocity Index** — ranks users using accuracy, average response time, and response-time consistency.
* **Fatigue Analysis** — analyzes accuracy and response time across sequential question groups.
* **Question Difficulty Index** — ranks questions using attempts, accuracy, and average response time.

Analytics are implemented using **MongoDB aggregation pipelines**.

## Seed Data

The seed script generates:

* 50 users
* 3 exams
* 10 subjects
* 30 chapters
* 500 questions

Run:

```bash
cd backend
python seed.py
```

`demo_analytics.py` generates question-attempt data for demonstrating the analytics APIs.

```bash
python demo_analytics.py
```

## Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `.env` from `.env.example` and configure MongoDB.

Start the API:

```bash
uvicorn app.main:app --reload
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## API

| Feature             | Endpoint                                         |
| ------------------- | ------------------------------------------------ |
| Exams               | `GET /api/exams`                                 |
| Subjects            | `GET /api/exams/{exam_id}/subjects`              |
| Chapters            | `GET /api/subjects/{subject_id}/chapters`        |
| Quiz                | `GET /api/quiz/{chapter_id}`                     |
| Submit Answer       | `POST /api/quiz/submit`                          |
| Result              | `GET /api/quiz/{quiz_id}/result`                 |
| Learning Velocity   | `GET /api/analytics/learning-velocity`           |
| Fatigue Analysis    | `GET /api/analytics/fatigue/{user_id}/{quiz_id}` |
| Question Difficulty | `GET /api/analytics/question-difficulty`         |

## Testing

Run the backend tests:

```bash
cd backend
pytest -q
```

Build the frontend:

```bash
cd frontend
npm run build
```

## Project Structure

```text
backend/
├── app/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   ├── config.py
│   ├── database.py
│   └── main.py
├── tests/
├── seed.py
├── demo_analytics.py
└── requirements.txt

frontend/
└── src/
    ├── App.tsx
    ├── index.css
    └── main.tsx
```

## Design Notes

* Authentication is intentionally dummy as permitted by the assignment.
* Question attempts are treated as event data for analytics.
* Analytics are calculated from stored attempt events rather than hard-coded results.
* MongoDB aggregation pipelines are used for analytical calculations.
