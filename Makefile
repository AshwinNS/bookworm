ifneq (, $(wildcard env/.env.dev))
	include env/.env.dev
	export
else
	$(error env/.env.dev file is required but not found.)
endif


.PHONY: help build down destroy restart log ps pull-model test
help:
	@echo "Please use 'make <target>', where <target> is one of"
	@echo ""
	@echo "  build                 		Build and start all containers"
	@echo "  down                  		Stop and remove all containers"
	@echo "  destroy               		Stop and remove all containers including volumes"
	@echo "  restart c=<service>   		Restart all containers or only mentioned containers"
	@echo "  log c=<service>       		View container logs"
	@echo "  ps                    		View active containers"
	@echo "  pull-model     			Pull the model from Ollama"
	@echo "  setup                 		Build containers and pull Ollama model"
	@echo "  test              			Run unit tests"
	@echo ""

setup: build pull-model
	@echo "Running build target..."
	@make build
	@echo "Running pull-model target..."
	@make pull-model
	@echo "Setup complete."
build:
	docker compose up -d --build
down:
	docker compose down
destroy:
	docker compose down -v
restart:
	docker compose stop $(c)
	docker compose up -d $(c)
log:
	docker compose logs --tail=100 -f $(c)
ps:
	docker compose ps
pull-model:
	@echo "Pulling the model from Ollama..."
	@if [ -z "$(MODEL_NAME)" ]; then \
		echo "MODEL_NAME is not set. Using default value 'llama3.2'."; \
		MODEL_NAME="llama3.2"; \
	fi; \
	if ! docker ps --format '{{.Names}}' | grep -q '^bookworm-ai$$'; then \
		echo "Error: Container 'bookworm-ai' is not running. Please start the container first."; \
		exit 1; \
	fi; \
	
	docker exec -it bookworm-ai ollama pull $$MODEL_NAME
test:
	@echo "Running tests..."
	@if ! docker ps --format '{{.Names}}' | grep -q '^bookworm-api$$'; then \
		echo "Error: Container 'bookworm-api' is not running. Please start the container first."; \
		exit 1; \
	fi; \
	docker exec -it bookworm-api pytest -v --disable-warnings api/tests
