# AGENTS.md

## Developer commands

### Backend (Django)
```bash
cd backend
source venv/Scripts/activate    # Windows venv path — not venv/bin
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
npm run build    # output → dist/
```

Start both servers simultaneously — the frontend fetches from `http://localhost:8000/api`.

## Architecture

**Backend:** Django 6.0.4 + DRF 3.17.1, three apps under `backend/`:
- `users/` — `UserProfile` (OneToOne to Django User, adds phone)
- `resources/` — `ResourceType`, `Resource` (only `is_active=True` exposed)
- `reservations/` — `Reservation` model with overlap detection in `clean()` + `full_clean()` called in `save()`

**API routes** (all under `/api/`):
| Path | Method | Description |
|---|---|---|
| `/api/reservations/` | GET, POST | List or create reservations |
| `/api/resources/` | GET | Active resources only |
| `/api/resource-types/` | GET | All resource types |
| `/api/users/` | GET | Temp endpoint — removed in Etapa 5 |

**Frontend:** React 19 + Vite + React Router v7. Pages in `src/pages/`, shared components in `src/components/`, API calls in `src/services/reservationsService.js`. Routes: `/`, `/new`, `/about`.

## Critical gotchas

- **No auth yet (Etapa 3).** Frontend hardcodes `PLACEHOLDER_USER_ID = 1` in `NewReservationPage.jsx`. Backend uses `AllowAny` permissions. Do not add auth until Etapa 5.
- **API_BASE** is hardcoded to `http://localhost:8000/api` in `reservationsService.js` — not in env vars.
- **Overlap detection** runs in `Reservation.clean()` and is enforced in `save()` via `full_clean()`. Condition: `start_time < other.end_time AND end_time > other.start_time` on same resource/date, excluding `cancelled` status.
- **No DELETE endpoint** for reservations.
- **SQLite** for dev (`db.sqlite3`). README says PostgreSQL for prod but not configured yet.
- **Windows venv path** is `venv/Scripts/activate` — the repo was set up on Windows.

## Git workflow

Branch strategy: `main` (stable) ← `develop` (active) ← `feature/*` (PRs into develop).
`develop` has branch protection on GitHub — no direct pushes.
Commit convention: `feat:`, `fix:`, `refactor:`, `docs:`

## Existing instructions

- `CLAUDE.md` — more detailed architecture reference
