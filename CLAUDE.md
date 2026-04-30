# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Club Reservas System — a concurrent reservation system for club resources. The core business problem is preventing overlapping reservations (time-slot conflict detection). Currently in **Etapa 3** (Stage 3); Etapa 5 will add authentication.

## Commands

### Backend (Django)

```bash
cd backend
source venv/Scripts/activate   # Windows venv activation

python manage.py runserver     # Dev server at http://localhost:8000
python manage.py migrate
python manage.py createsuperuser
python manage.py test          # Run backend tests
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev      # Dev server at http://localhost:5173
npm run build
npm run lint     # ESLint
```

## Architecture

**Stack:** Django 6.0.4 + DRF 3.17.1 backend, React 19 + Vite frontend, SQLite (dev). CORS configured for `localhost:5173`.

### Backend Structure

`backend/config/` — Django settings and root URL config.  
Three apps, each with models, serializers, views, URLs:

- `users/` — extends Django's built-in User with a `UserProfile` (OneToOne, adds phone)
- `resources/` — `ResourceType` and `Resource` models; only active resources are exposed via API
- `reservations/` — core app; `Reservation` model with overlap detection

**API routes** (all under `/api/`):

| Method | Path | Description |
|---|---|---|
| GET/POST | `/api/reservations/` | List or create reservations |
| GET | `/api/resources/` | Active resources only |
| GET | `/api/resource-types/` | All resource types |
| GET | `/api/users/` | Temp endpoint, removed in Etapa 5 |

Views use DRF generic views (`ListCreateAPIView`, `ListAPIView`) with `select_related()` for FK fields.

**Reservation conflict detection** lives in `Reservation.clean()` and is enforced in `save()` via `full_clean()`. Overlap condition: `start_time < other.end_time AND end_time > other.start_time` on the same resource and date, excluding the current instance.

### Frontend Structure

`src/pages/` — full-page components (`ReservationsPage`, `NewReservationPage`, `AboutPage`).  
`src/components/` — reusable UI (`ReservationItem`).  
`src/services/reservationsService.js` — all fetch calls to the backend API.  
`src/App.jsx` — React Router v7 routes: `/`, `/new`, `/about`.

**Auth placeholder:** `PLACEHOLDER_USER_ID = 1` is hardcoded in the frontend until authentication is implemented in Etapa 5. On the backend, `request.user` will eventually replace this.

### Key Patterns

- Serializers expose read-only computed fields (e.g., `resource_name`, `user_username`) via `SerializerMethodField` or explicit `read_only=True`.
- Reservation status choices: `pending`, `confirmed`, `cancelled`.
- No DELETE endpoint for reservations yet.
- No Docker, no CI/CD pipeline configured.

## Commit Convention

```
feat:, fix:, refactor:, docs:
```

Branch strategy: `main` (stable), `develop` (active), `feature/*` branches with PRs into develop.
