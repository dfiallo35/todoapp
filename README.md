# Task App

This is a simple task app built with FastAPI and PostgreSQL.


## Setup

1. Install [uv](https://docs.astral.sh/uv/) if you don’t have it yet.
2. Install the dependencies with `uv sync`.
3. Create a `.env` file with the following content:

```dotenv
DATABASE_URL=postgresql+asyncpg://postgres:postgrespassword@localhost:5440/todoapp
```

4. Install [docker](https://docs.docker.com/engine/install/) and [docker-compose](https://docs.docker.com/compose/install/) then run `docker-compose -f docker-compose-dev.yml up -d` to start the database.
5. Intall [alembic](https://alembic.sqlalchemy.org/en/latest/tutorial.html#install-alembic)then run the migrations with `uv run alembic upgrade head`.
6. Run the app with `uv run fastapi dev`.


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
