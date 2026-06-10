# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Club Reservas System — a concurrent reservation system for club resources. The core business problem is preventing overlapping reservations (time-slot conflict detection). Currently in **Etapa 5** (authentication complete).

## Commands

### Backend (Django)

```bash
cd backend
source venv/Scripts/activate   # Windows venv activation

python manage.py runserver     # Dev server at http://localhost:8000
python manage.py migrate
python manage.py createsuperuser
python manage.py test          # Run backend tests (49 tests)
```

### Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev      # Dev server at http://localhost:5173
npm run build
npm run lint     # ESLint (flat config, TypeScript + JS)
```

## Architecture

**Stack:** Django 6.0.4 + DRF 3.17.1 + SimpleJWT 5.5.1 backend, React 19 + Vite frontend, SQLite (dev). CORS configured for `localhost:5173`.

### Backend Structure

`backend/config/` — Django settings and root URL config.  
Three apps, each with models, serializers, views, URLs:

- `users/` — extends Django's built-in User with a `UserProfile` (OneToOne, adds phone), auth endpoints (login/register)
- `resources/` — `ResourceType` and `Resource` models; only active resources are exposed via API (public - no auth required)
- `reservations/` — core app; `Reservation` model with overlap detection

**API routes** (all under `/api/`):

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/auth/login/` | No | Login, returns JWT |
| POST | `/api/auth/register/` | No | Register, returns JWT |
| GET/POST | `/api/reservations/` | Yes | List or create reservations |
| GET/PATCH/DELETE | `/api/reservations/<id>/` | Yes | Detail, update, or delete |
| GET | `/api/resources/` | No | Active resources only |
| GET | `/api/resource-types/` | No | All resource types |

Views use `@api_view` decorators with `select_related()` for FK fields.

**Reservation conflict detection** lives in `Reservation.clean()` and is enforced in `save()` via `full_clean()`. Overlap condition: `start_time < other.end_time AND end_time > other.start_time` on the same resource and date, excluding `cancelled` status + self.

**Serializers** catch `ValidationError` from model `full_clean()` in `create()`/`update()` and re-raise as DRF `ValidationError` (prevents 500 instead of 400).

### Frontend Structure

`src/pages/` — full-page components (`ReservationsPage`, `NewReservationPage`, `AboutPage`, `LoginPage`, `RegisterPage`).  
`src/components/` — reusable UI (`ReservationItem`, `ProtectedRoute`).  
`src/services/` — API client (`api.ts`, `authService.ts`, `recursoService.ts`, `reservaService.ts`).  
`src/contexts/` — React context (`AuthContext.tsx`).  
`src/types/` — TypeScript type definitions.

**Auth:** JWT stored in localStorage. `AuthContext` decodes token on mount. `ProtectedRoute` redirects to `/login` when unauthenticated. New reservations use the authenticated user instead of hardcoded ID.

### Key Patterns

- Serializers expose read-only computed fields (`resource_name`, `user_username`) via `source=` kwarg.
- Reservation status choices: `pending`, `confirmed`, `cancelled`.
- DELETE endpoint removes reservation permanently (204). PATCH with `{"status": "cancelled"}` for soft cancel.
- No Docker, no CI/CD pipeline configured.

## Commit Convention

```
feat:, fix:, refactor:, docs:
```

Branch strategy: `main` (stable), `develop` (active), `feature/*` branches with PRs into develop.
