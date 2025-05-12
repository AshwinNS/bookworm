[![Makefile CI](https://github.com/AshwinNS/bookworm/actions/workflows/main.yml/badge.svg)](https://github.com/AshwinNS/bookworm/actions/workflows/main.yml)

# Bookworm
Bookworm is a FastAPI based book management api with AI recommendation system (postgres as database). It's easy to deploy, manage and scale. As the project is solo maintained `github copilot` is used for reviewer for basic code reviews.

## Prerequisites

Before you begin, you'll need to install one important software:

### Install docker
Docker is required to run the application, visit [docker for desktop](https://www.docker.com/products/docker-desktop/) and follow the steps.

> [!IMPORTANT]
> For the application to deploy `.env.dev` file should be configured properly. Check [env/README.md](env/README.md) before proceeding.

## Running the application

The following commands will help developers to spin-up the bookworm app local dev server. You have two command options for running bookworm, using `Docker` or `Make`.

### Option 1: Using Docker command

#### 1. Clean-up (optional step, remove created volumes and containers if any)

```bash
docker compose down -v
```

1. Build and setup application
```bash
docker compose up -d --build
```

This command will do the following.
1. Build docker image and deploy `api`, `db`, `ai` and `redis` services.
2. Start up the database.
3. Run api using uvicorn in port `8000`.

#### 2. Pull model from ollama for `ai` service to use
```bash
docker exec -it bookworm-ai ollama pull llama3.2
```
> [!NOTE]
>  change the llm model name according to value provided in `.env.*` file default is set to `llama3.2`

#### 3. Load sample data to db (optional step)
```bash
docker exec -i pg-db psql -U postgres books < utils/data/db_loader.sql
```


### Option 2: Using Make command

#### 1. Clean-up (optional step)
```bash
make destroy
```

#### 2. Build and setup end to end application including local llm service.
```bash
make setup
```

> [!NOTE]
> `make setup` is a collection of 3 targets. It `builds` the application first, the `pull-model` downloads the llm from the ollama hub and finally `load_data` load the db with some books data. Additionally a `books_admin` user also will be added out of the box.

### Features to be added

- Use `uv` or `poetry` package for dependency management.
- Implement `pgai` for book recommendation.
