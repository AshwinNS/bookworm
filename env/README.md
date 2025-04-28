# Env files

`Bookworm` application is driven using the env files. I have kept separate env file for development instance with name `.env.dev`, similarly we can make `.env.prod` to segregate env variables per instances. This doc will provide you with a basic `.env.dev` file structure, with which you can spin-up your development instance. 

> [!WARNING]  
> Do not check-in `.env*` files to the repo. `.env*` is already part of `.gitignore`.

## Development instance
### File: env/.env.dev

```
# Django Variables
# Change any value if required to personalize
DEBUG=1
ENVIRONMENT_AREA=DEVELOPMENT

# Database secret
POSTGRES_DB=books
POSTGRES_TEST_DB=TEST
SQL_HOST=db
SQL_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=HfG3fj0OfjvHdkf234ja
DB_ENGINE=postgresql
DATABASE=pgdb

# Python Confs
PYTHONDONTWRITEBYTECODE=1
PYTHONUNBUFFERED=1

# AI related
# Get your model from https://ollama.com/library
MODEL_NAME=llama3.2
```
