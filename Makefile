.PHONY: help install dev-setup up down logs test lint format clean

help:
	@echo "Cybersecurity Fraud Detection System - Commands"
	@echo "================================================"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make install        - Install dependencies"
	@echo "  make dev-setup      - Setup development environment"
	@echo ""
	@echo "Docker Commands:"
	@echo "  make up             - Start all services"
	@echo "  make down           - Stop all services"
	@echo "  make logs           - View API logs"
	@echo "  make clean          - Remove containers and volumes"
	@echo ""
	@echo "Development:"
	@echo "  make dev            - Start development server"
	@echo "  make test           - Run tests"
	@echo "  make test-coverage  - Run tests with coverage"
	@echo "  make lint           - Run code linting"
	@echo "  make format         - Format code"
	@echo ""
	@echo "Scripts:"
	@echo "  make client         - Run example client"
	@echo "  make train          - Train ML models"
	@echo ""

install:
	pip install -r requirements.txt

dev-setup: install
	cp .env.example .env
	mkdir -p logs models data
	@echo "Development environment setup complete!"

up:
	docker-compose up -d

down:
	docker-compose down

logs:
	docker-compose logs -f api

test:
	pytest tests/ -v

test-coverage:
	pytest tests/ --cov=src --cov-report=html
	@echo "Coverage report generated in htmlcov/"

lint:
	flake8 src/ tests/ --max-line-length=100
	pylint src/ --disable=all --enable=E,F

format:
	black src/ tests/ scripts/
	isort src/ tests/ scripts/

dev:
	python -m uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

client:
	python scripts/client_example.py

train:
	python scripts/train_models.py --data data/training_data/transactions.csv

build:
	docker-compose build

ps:
	docker-compose ps

shell-api:
	docker-compose exec api bash

shell-db:
	docker-compose exec db psql -U fraud_user fraud_detection_db

backup-db:
	docker-compose exec db pg_dump -U fraud_user fraud_detection_db > backup.sql

restore-db:
	docker-compose exec -T db psql -U fraud_user fraud_detection_db < backup.sql

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache .coverage htmlcov

setup: dev-setup up
	@echo ""
	@echo "Setup complete! Services starting..."
	@sleep 5
	@echo ""
	@echo "API available at: http://localhost:8000"
	@echo "API Docs at: http://localhost:8000/docs"
	@echo "Grafana at: http://localhost:3000"

.DEFAULT_GOAL := help
