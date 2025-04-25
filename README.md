# Bookworm
Bookworm is a book management api with AI recommendation system. It's easy to deploy, manage and scale.

> [!IMPORTANT]  
> For the application to deploy `.env*` file should be configured properly. Check [env/README.md](env/README.md) before proceeding.

## Development server spin-up

The following commands will help developers to spin-up the bookworm app local dev server. Both `make` commands and `docker compose` commands are provided with description.

* Clean-up (remove created volumes and containers if any)
```bash
# docker command
docker compose down -v

# make command
make destroy
```

* Build and setup end to end application including local ollama
```bash
# make command
make setup

# docker commands
docker compose up -d --build
docker exec -it bookworm-ai ollama pull <model-name>
```

* Build the application.
```bash
# docker command
docker compose up -d --build

# make command
make build
```
Build command will do the following in the background.
1. Build docker image and deploy `api`, `db` and `ai` services.
2. Start up the database.
3. Run api using uvicorn.

* Pull model from ollama
```bash
# run docker command only after containers are up
docker exec -it bookworm-ai ollama pull <model-name>

# make command, this will pull model mentioned in MODEL_NAME env var
make pull-model
```