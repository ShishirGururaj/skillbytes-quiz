# SkillBytes Quiz Application

A WhatsApp-style quiz application built with React, FastAPI, and MongoDB.

## Stack

- React
- TypeScript
- FastAPI
- Python
- MongoDB
- Pydantic

## Architecture

The application follows a lightweight layered architecture:

- React frontend for the quiz experience
- FastAPI backend for REST APIs
- MongoDB for application and event data
- MongoDB aggregation pipelines for analytics

## Application Flow

Login → Exam → Subject → Chapter → Quiz → Result

## Database Collections

- `users`
- `exams`
- `subjects`
- `chapters`
- `questions`
- `attempts`

The `attempts` collection will capture every question-level interaction and will serve as the source of truth for analytics.

## Seed Data

The seed script generates:

- 50 users
- 3 exams
- 10 subjects
- 30 chapters
- 500 questions

The seed data is deterministic to make local development and testing reproducible.

## Local Setup

### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt