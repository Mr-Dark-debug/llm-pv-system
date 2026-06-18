# Implementation Tasks

## Completed Build Tasks

- [x] Create uv virtual environment and requirements.
- [x] Add FastAPI app factory and single-command `run.py`.
- [x] Add SQLAlchemy database session dependency, table creation, and seed initialization.
- [x] Add ORM models for users, participants, LLM models, prompts, responses, PV detections, survey responses, forced-choice responses, translations, acceptability judgements, and analysis cache.
- [x] Seed 16+ LLM models and 90 benchmark prompts.
- [x] Implement OOP service layer: `LLMClient`, `PVDetector`, `BenchmarkRunner`, `SurveyService`, `LEICalculator`, `PVACalculator`, `AnalysisService`, `ExportService`.
- [x] Add Pydantic v2 request/response schemas.
- [x] Add HTML page routes using Jinja2.
- [x] Add JSON API routes for benchmark, survey, analysis, and export.
- [x] Add Bootstrap 5 frontend templates and Chart.js visualizations.
- [x] Add vanilla JavaScript for benchmark runs, survey submission, and charts.
- [x] Add README, `.env.example`, design notes, and tests.

## Research-Deployment Follow-Ups

- [ ] Replace the included PHaVE-style starter list with the exact study-approved PHaVE list.
- [ ] Add a human annotation workflow for Layer 3 double annotation and adjudication.
- [ ] Add real SDK implementations in `LLMClient` for each provider once API keys and model-access policies are confirmed.
- [ ] Replace generated prompt seed text with the final preregistered prompt wording if it differs from this implementation.
- [ ] Add authentication for admin/researcher routes before collecting real participants.
