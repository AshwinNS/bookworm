# Bookworm
Bookworm is a book management api with AI recommendation system. It's easy to deploy, manage and scale.

> [!IMPORTANT]  
> For the application to deploy `.env*` file should be configured properly. Check [env/README.md](env/README.md) before proceeding.

## Development server spin-up

The following commands will help developers to spin-up the bookworm app local dev server
* Clean-up (remove created volumes and containers if any)
```bash
docker compose down -v
```

* Build the application.
```bash
docker compose up -d --build
```
Build command will do the following in the background.
1. Build docker image and deploy `api` and `db` services.
2. Start up the database.
3. Run api using uvicorn.
