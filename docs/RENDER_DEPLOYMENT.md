# Render Deployment

This app is ready for Render as a Python web service.

## Required Settings

- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/healthz`
- Python version: `3.11.9`

## SQLite Persistence

The included `render.yaml` mounts a persistent disk at:

```text
/opt/render/project/src/data
```

and sets:

```text
DATABASE_URL=sqlite:////opt/render/project/src/data/lei_evaluation.db
```

Without a persistent disk, SQLite data on Render can disappear on redeploys. For real participant collection, either keep the disk attached or migrate to managed Postgres.

## Environment Variables

Optional provider keys:

- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`
- `GOOGLE_API_KEY`
- `GROQ_API_KEY`
- `OPENROUTER_API_KEY`

The app still boots without keys and clearly marks generated benchmark text as mock output.

## Official References

- Render FastAPI deployment: https://render.com/docs/deploy-fastapi
- Render web-service port binding: https://render.com/docs/web-services#port-binding
- Render environment variables: https://render.com/docs/environment-variables
- Render persistent disks: https://render.com/docs/disks
