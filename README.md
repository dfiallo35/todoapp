# Todo App

This is a simple todo app built with FastAPI and PostgreSQL.


## Setup

1. Install [uv](https://docs.astral.sh/uv/) if you don’t have it yet.
2. Install the dependencies with `uv sync`.


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
