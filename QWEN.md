# Project Context for Qwen Code

This document provides essential context about the 'JP - JobPilot Career Assistant' project for efficient interaction with Qwen Code.

## Project Overview

- **Name:** JP - JobPilot Career Assistant
- **Description:** A clean and maintainable career assistance platform focused on job searching and career networking.
- **Type:** Full-stack web application
- **Primary Technologies:**
  - **Backend:** Python 3.12+, FastAPI, SQLAlchemy, Pydantic
  - **Frontend:** TypeScript, SolidJS, Vite, TailwindCSS, DaisyUI
  - **Database:** SQLite (development), potentially PostgreSQL (production intent inferred from backend stack)
  - **Testing:** Pytest (Python), Vitest (JS), Playwright (E2E)

## Project Structure

The project is organized into distinct backend and frontend directories:

- `backend/`: Contains the Python FastAPI application.
  - `api/`: Core API logic, including `main.py`, `routers`, `models`, and `config.py`.
  - `data/`: Likely contains database files or data management scripts.
  - `services/`: Business logic layer.
  - `utils/`: Utility functions.
- `frontend/`: Contains the SolidJS/Vite/TypeScript frontend application.
  - `src/`: Main source code for components, routes, and application logic.
  - `public/`: Static assets.
  - `dist/`: Built production files.
- `tests/`: Contains Python tests for the backend.
- `web-bundles/`: (Likely related to deployment or build artifacts).
- Root-level scripts for running, testing, and managing the application (e.g., `run_all.bat`, `run_all.sh`, `start_dev_servers.bat`).

## Running the Application

There are multiple ways to start the development servers:

### Recommended Method (Windows)

1.  **Start Servers:** Run `start_dev_servers.bat`. This starts the backend and frontend servers in separate windows.
2.  **Stop Servers:** Run `stop_dev_servers.bat`.

### Alternative Methods (Cross-Platform)

- **Run Both Servers (Foreground):**
  ```bash
  # Linux/Mac
  ./run_all.sh
  # Windows
  run_all.bat
  ```
  Press Ctrl+C to stop.

- **Run Both Servers (Background/Subprocess):**
  ```bash
  # Linux/Mac
  ./run_all.sh --subprocess
  # Windows
  run_all.bat --subprocess
  ```

## Development Workflow

### Backend (Python/FastAPI)

- **Entry Point:** `backend/api/main.py`
- **Dependencies:** Managed via `pyproject.toml`. Install with `pip install -e .` or similar.
- **Configuration:** `backend/api/config.py` (uses Pydantic Settings, can load `.env`).
- **Code Style/Linting:** Black, Ruff (configured in `pyproject.toml`).
- **Testing:** Use `pytest` (configured in `pyproject.toml` and `pytest.ini`).

### Frontend (TypeScript/SolidJS/Vite)

- **Entry Point:** Defined in `frontend/src` (likely `index.tsx` or similar).
- **Dependencies:** Managed via `frontend/package.json`. Install with `cd frontend && npm install`.
- **Development Server:** `cd frontend && npm run dev` (Vite).
- **Build:** `cd frontend && npm run build`.
- **Testing:** `npm run test` (Vitest), `npm run test:e2e` (Playwright).

## Key Documentation Files

- `README.md`: General project overview and quickstart.
- `frontend_development_guide.md`: Details on frontend tech stack, structure, and workflow.
- Various checklist and analysis files (e.g., `api_handler_checklist.md`, `frontend_handler_checklist.md`, `playwright_testing_approach.md`) provide specific guidance and standards for development tasks.