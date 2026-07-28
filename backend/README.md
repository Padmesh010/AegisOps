# AegisOps Core Backend

Enterprise AI-Powered DevOps Observability & Automation Platform Backend.

## Tech Stack
*   **Python 3.11+**
*   **FastAPI** (Web Framework)
*   **SQLAlchemy 2.x & Alembic** (Asyncpg PostgreSQL ORM)
*   **Redis** (Rate-limiting & caching)
*   **Pytest** (Testing suite)
*   **Ruff & MyPy** (Linting, formatting, static analysis)

## Local Setup
1.  Ensure you have **Poetry** installed.
2.  Install dependencies:
    ```bash
    poetry install
    ```
3.  Run code style checks:
    ```bash
    poetry run ruff check .
    poetry run mypy .
    ```
4.  Run testing suite:
    ```bash
    poetry run pytest -v
    ```
5.  Start backend locally:
    ```bash
    poetry run uvicorn app.main:app --port 8000 --reload
    ```
    Access Swagger API Docs at `http://localhost:8000/docs`.
