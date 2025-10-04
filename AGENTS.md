# Repository Guidelines

## Project Structure & Module Organization
- `backend/` holds the FastAPI service; keep routers in `app/routers`, shared helpers in `app/utils`, and DTOs in `app/models` or `app/schemas`; wire new routers through `app/main.py`.
- `backend/run.py` loads `.env` and configures uvicorn; reuse its logging setup when bootstrapping background tasks or scripts.
- `frontend/` is the Vite/Vue client; add views to `src/views`, shared UI to `src/components`, state to `src/store`, and keep logger helpers under `src/utils/logger.js`. Update `doc/` alongside functional changes.

## Build, Test, and Development Commands
- Backend env: `python -m venv venv` -> activate -> `pip install -r backend/requirements.txt`.
- Start the API with `python backend/run.py` (auto loads `.env`) or `uvicorn app.main:app --reload --app-dir backend/app`.
- Frontend workflow: `cd frontend && npm install`, then `npm run dev` locally, `npm run build` for production bundles, `npm run preview` to smoke-test output.
- Quick demos: `backend/start.bat` (Windows) or `backend/start.sh` (Unix).

## Coding Style & Naming Conventions
- Python uses 4-space indents, `snake_case` functions, `PascalCase` Pydantic models; keep type hints and log through `app.utils.logger.get_logger` for emoji-rich structured output.
- Vue/JS follow ES module syntax, `<script setup>`, PascalCase component filenames, and camelCase Pinia stores; place shared helpers in `src/utils`.
- Secrets live in `.env` copied from `.env.example`; never commit `.env` or generated `logs/` artifacts.

## Testing Guidelines
- API tests belong in `backend/tests/` with `pytest` plus `httpx.AsyncClient`; cover happy and edge paths, isolating SQLite data per test.
- Frontend tests should live in `frontend/src/__tests__/` using Vitest or Vue Test Utils; snapshot Ant Design Vue surfaces when layouts shift.
- Document any manual checks in the PR when automated coverage is pending.

## Commit & Pull Request Guidelines
- Follow Conventional Commits seen in history (e.g., `feat(logging): add request tracing`); keep summaries <=72 characters and scope changes whenever touching a specific module.
- PRs must note intent, commands run (`pytest`, `npm run build`), config updates, and include before/after visuals for UI tweaks.
- Link issues, request cross-team review for backend+frontend edits, and ensure CI (Docker build workflow) is green before merging.

## Security & Configuration Tips
- Review `.env.example` for required keys (`SECRET_KEY`, `ALLOWED_ORIGINS`) and keep environment-specific values outside version control.
- Mirror the CORS whitelist in `app/main.py` for new services and redact sensitive payloads before calling `logger.debug`.
