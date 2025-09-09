# Task App

This is a simple task management application built with FastAPI and PostgreSQL. It follows a 4-layer architecture (Presentation, Application, Domain, and Infrastructure) to ensure clean separation of concerns and maintainable code.

Key features include:
- CRUD operations for tasks: create, read, update, and delete tasks.
- User authentication with JWT tokens for secure access.
- iltering, pagination, and sorting on task lists.
- Async database operations using SQLAlchemy with asyncpg for high performance.
- Dependency injection for decoupled services and repositories.
- Dockerized development environment with Postgres for easy setup and reproducibility.

## Setup

1. Install [uv](https://docs.astral.sh/uv/) if you don’t have it yet.
2. Install the dependencies with `uv sync`.
3. Create a `.env` file with the following content:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:postgrespassword@localhost:5440/todoapp
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256
SECRET_KEY=<supersecret>
```

4. Create the secrets key with `openssl rand -hex 64` and replace `<supersecret>` with the output.
5. Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) then run `docker-compose -f docker-compose-dev.yml up -d` to start the database.
6. Intall [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#install-alembic)then run the migrations with `uv run alembic upgrade head`.
7. Run the app with `uv run fastapi dev`.


## Pre-Commit

We use [pre-commit](https://pre-commit.com/) to keep code clean.

Install the hooks after cloning:

```bash
uv run pre-commit install
```

Run checks on all files:

```bash
uv run pre-commit run --all-files
```
