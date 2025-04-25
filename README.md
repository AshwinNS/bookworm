# Bookworm
Bookworm is a book management api with AI recommendation system. It's easy to deploy, manage and scale.

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

#### 2. Build application
```bash
docker compose up -d --build
```

this command will do the following in the background.
1. Build docker image and deploy `api`, `db` and `ai` services.
2. Start up the database.
3. Run api using uvicorn in port `8000`.

#### 3. Pull model from ollama for `ai` service to use
```bash
docker exec -it bookworm-ai ollama pull llama3.2
```
> [!NOTE]
>  change the llm model name according to value provided in `.env.*` file default is set to `llama3.2`

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
> If faced with error check make targets to debug
