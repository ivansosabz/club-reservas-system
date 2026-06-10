# AGENTS.md

## Developer commands

### Backend (Django)
```bash
cd backend
source venv/Scripts/activate    # Windows venv path
python manage.py runserver      # http://localhost:8000
python manage.py migrate
python manage.py test
pip install -r requirements.txt # initial setup
```

### Frontend (React + Vite)
```bash
cd frontend
npm install
npm run dev      # http://localhost:5173
npm run lint     # ESLint flat config (eslint.config.js)
npm run build    # output -> dist/
```

Start both servers simultaneously.

## Architecture

**Backend:** Django 6.0.4 + DRF 3.17.1 + SimpleJWT 5.5.1, three apps under `backend/`:
- `users/` — `UserProfile` (OneToOne to Django User, adds phone), auth endpoints
- `resources/` — `ResourceType`, `Resource` (only `is_active=True` exposed)
- `reservations/` — `Reservation` model with overlap detection in `clean()` + `full_clean()` called in `save()`

**API routes:**

| Path | Method | Auth | Description |
|---|---|---|---|
| `/api/auth/login/` | POST | No | Login, returns JWT |
| `/api/auth/register/` | POST | No | Register, returns JWT |
| `/api/reservations/` | GET, POST | Yes | List or create reservations |
| `/api/reservations/<id>/` | GET, PATCH, DELETE | Yes | Detail, update, or delete |
| `/api/resources/` | GET | No | Active resources only |
| `/api/resource-types/` | GET | No | All resource types |

**Frontend:** React 19 + Vite + React Router v7. Pages in `src/pages/`, shared components in `src/components/`, API calls in `src/services/`, auth state in `src/contexts/AuthContext.tsx`. Routes: `/`, `/new`, `/about`, `/login`, `/register`. Protected routes redirect to `/login`.

## Auth flow

- Login/register returns `{access, refresh, user}`. Frontend stores `access` token in localStorage.
- Every API call attaches `Authorization: Bearer <token>` via `api.ts`.
- JWT payload includes `user_id` and `username` via custom serializer.
- `AuthContext` decodes token on mount to restore session.
- `ProtectedRoute` wraps pages that require authentication.

## Critical details

- **Overlap detection** runs in `Reservation.clean()` via `full_clean()` in `save()`. Condition: `start_time < other.end_time AND end_time > other.start_time` on same resource/date, excluding `cancelled` + self.
- **Serializers** catch `ValidationError` from model `full_clean()` and re-raise as DRF `ValidationError` (otherwise returns 500 instead of 400).
- **SQLite** for dev (`db.sqlite3`). PostgreSQL planned for prod.
- **Windows venv path** is `venv/Scripts/activate`.
- **API_BASE** hardcoded to `http://localhost:8000/api` in `api.ts`.

## Tests

49 backend tests across 3 apps:
- `users/`: UserProfile model + auth endpoints (login, register, permissions)
- `resources/`: Resource/ResourceType models + API active filter
- `reservations/`: Overlap detection (9 scenarios), CRUD API, DELETE, permissions

## Git workflow

Branch strategy: `main` (stable) <- `develop` (active) <- `feature/*` (PRs into develop).
`develop` has branch protection on GitHub — no direct pushes.
Commit convention: `feat:`, `fix:`, `refactor:`, `docs:`
