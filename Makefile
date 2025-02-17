.PHONY: run/up run/down run/detached run/shell run/manage run/logs help install test check lint pylint types format migrate run/bootstrap-test

run/up:
	docker compose up --build

run/down:
	docker compose down

run/detached:
	docker compose up --build -d

run/shell:
	docker exec -it emol-app-1 /bin/bash

run/manage:
	@read -p "Enter management command: " command && \
	docker exec -it emol-app-1 poetry run python manage.py $$command

run/logs:
	docker compose logs -f app

help:
	@grep -E '^[a-zA-Z0-9/-]+:.*?## .*$$' Makefile | sort | \
		while read -r line; do \
			command=$$(echo "$$line" | cut -d':' -f1); \
			help_text=$$(echo "$$line" | cut -d'#' -f2- | sed -e 's/## //'); \
			printf "%-20s %s\n" "$$command" "$$help_text"; \
		done

.DEFAULT_GOAL := help

install: ## Install project dependencies with poetry
	poetry install

test: install ## Run tests
	poetry run python manage.py test

check: check/format check/types check/lint check/test ## Run all checks (format, types, lint, test)

check/format: format ## Check code format (black, isort)
	@echo "Running format check..."
	poetry run black --check --diff .
	poetry run isort --check --diff .

check/types: types ## Check types with mypy
	@echo "Running type check..."
	poetry run mypy .

check/lint: lint ## Run linters (flake8)
	@echo "Running lint check..."
	poetry run flake8 .

check/test: test ## Run tests
	@echo "Running tests..."
	$(MAKE) test

lint: install ## Run flake8 linter
	poetry run flake8 .

pylint: install ## Run pylint linter (more strict)
	@touch __init__.py
	@poetry run pylint emol; status=$$?; rm -f __init__.py; exit $$status

types: install ## Run mypy type checker
	poetry run mypy .

format: install ## Format code with black and isort
	poetry run black .
	poetry run isort .

migrate: install ## Run Django migrations
	poetry run python manage.py migrate

run/bootstrap-test: ## Run bootstrap.sh and deploy.sh in a local Ubuntu container
	@echo "Running bootstrap.sh in a local Ubuntu container..."
	docker run --rm -it \
		-v $(CURDIR):/app \
		ubuntu:22.04 \
		/bin/bash -c "cd /app/setup_files && ./bootstrap.sh"
	@echo "Running deploy.sh in a local Ubuntu container..."
	docker run --rm -it \
		-v $(CURDIR):/app \
		ubuntu:22.04 \
		/bin/bash -c "cd /app/setup_files && ./deploy.sh" 