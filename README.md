# LLMs as Linguistic Input Evaluation System

FastAPI + SQLite + Jinja2 platform for benchmarking phrasal-verb production across LLMs and measuring L2 learner phrasal-verb avoidance.

## Quick Start

```powershell
cd D:\projects\LEI-evaluation\llm_pv_system
uv venv .venv
uv pip install -r requirements.txt
.\.venv\Scripts\python run.py
```

Open `http://localhost:8000`.

If port `8000` is already in use, either stop the existing process or run:

```powershell
$env:PORT=8001
.\.venv\Scripts\python run.py
```

## What Is Included

- FastAPI backend with async route handlers.
- SQLAlchemy 2.0 ORM models for all required tables.
- SQLite persistence across restarts.
- Seed data for 16 active LLMs and 90 benchmark prompts.
- Mock-safe LLM generation when API keys are absent.
- Phrasal-verb detection with PHaVE-style transparency labels.
- Participant survey capture for Study 1 and Study 2.
- LEI and PVA score calculation.
- Analysis JSON and Chart.js visualizations.
- CSV/JSON exports.
- Pytest coverage for core boot, seed, detection, scoring, and survey behavior.

## Main Pages

- `/` dashboard
- `/benchmark` model benchmark table and run controls
- `/benchmark/{model_id}` per-model output details
- `/survey/study1` Study 1 participant survey
- `/survey/study2` Study 2 participant survey
- `/survey-links` protected share-link manager
- `/s/{token}` protected public survey link
- `/analysis` analysis charts
- `/participants` participant table
- `/prompts` prompt manager
- `/export` data exports

## JSON APIs

- `GET /api/benchmark/models`
- `POST /api/benchmark/run/{model_id}`
- `POST /api/survey/submit`
- `POST /api/survey/links`
- `GET /api/survey/links`
- `GET /api/analysis/summary`
- `GET /api/admin/export/participants.csv`
- `GET /api/admin/export/benchmark.json`

## Optional Transformer Parsing

The app includes `spacy`, but does not require `en_core_web_trf` to boot. To enable transformer parsing experiments:

```powershell
.\.venv\Scripts\python -m spacy download en_core_web_trf
```

Then extend `app/services/pv_detector.py` to prefer dependency matches and keep the current list-based fallback for startup safety.

## Tests

```powershell
cd D:\projects\LEI-evaluation\llm_pv_system
.\.venv\Scripts\python -m pytest -q
```

## Data

The default database is `lei_evaluation.db` in the project directory. Copy `.env.example` to `.env` to change `DATABASE_URL` or configure provider API keys.

## Notes

See `DESIGN_NOTES.md` for implementation decisions and ambiguities from the attached prompt.

## Render Deployment

The project includes `render.yaml`, `runtime.txt`, and `docs/RENDER_DEPLOYMENT.md`. Render start command:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```
