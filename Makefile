.PHONY: help install test lint format clean docker-build docker-run migrate superuser shell

help: ## Show this help message
	@echo "Legal Processes Management System - Available commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

install-dev: ## Install development dependencies
	pip install -r requirements-dev.txt

migrate: ## Run database migrations
	python manage.py makemigrations
	python manage.py migrate

superuser: ## Create superuser
	python manage.py createsuperuser

shell: ## Open Django shell
	python manage.py shell

test: ## Run tests
	pytest

test-cov: ## Run tests with coverage
	pytest --cov=processes --cov=parties --cov-report=html --cov-report=term-missing

test-watch: ## Run tests in watch mode
	pytest-watch

lint: ## Run linting
	flake8 processes parties legal_processes
	black --check processes parties legal_processes
	isort --check-only processes parties legal_processes

format: ## Format code
	black processes parties legal_processes
	isort processes parties legal_processes

clean: ## Clean up generated files
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf .coverage htmlcov/ .pytest_cache/

docker-build: ## Build Docker image
	docker build -t legal-processes .

docker-run: ## Run with Docker Compose
	docker-compose up --build

docker-stop: ## Stop Docker containers
	docker-compose down

docker-clean: ## Clean Docker containers and images
	docker-compose down -v
	docker system prune -f

collectstatic: ## Collect static files
	python manage.py collectstatic --noinput

import-data: ## Import sample data
	python manage.py import_processes sample_data/*.html

setup: install migrate superuser collectstatic ## Complete setup
	@echo "Setup completed! Run 'python manage.py runserver' to start the development server."

production-setup: ## Setup for production
	python manage.py migrate
	python manage.py collectstatic --noinput
	python manage.py check --deploy

security-check: ## Run security checks
	bandit -r processes/ parties/ legal_processes/
	safety check

pre-commit: ## Run pre-commit hooks
	pre-commit run --all-files

docs: ## Generate documentation
	sphinx-apidoc -o docs/source processes parties
	cd docs && make html

serve-docs: ## Serve documentation
	cd docs/_build/html && python -m http.server 8001

check: lint test ## Run all checks
	@echo "All checks passed!"

dev: ## Start development server
	python manage.py runserver

dev-docker: ## Start development server with Docker
	docker-compose -f docker-compose.yml up --build

prod: ## Start production server
	docker-compose -f docker-compose.prod.yml up --build -d 