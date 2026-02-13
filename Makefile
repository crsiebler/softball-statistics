# Makefile for softball-statistics

.PHONY: help setup install test run run-all clean format check-format lint pre-commit-install generate-test-data process-test-data generate-and-process-test-data

FILE ?= data/input/fray-cyclones-winter-01_2026-01-29.csv

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup:  ## Create conda environment (idempotent)
	conda env list | grep -q softball-stats || conda env create -f environment.yml

install:  ## Install package in development mode (creates console script)
	pip install -e .

test:  ## Run all unit tests
	pytest tests/ -v --cov=src --cov-report=html

run:  ## Run console script (requires install first)
	softball-stats --file $(FILE) --output data/output/stats.xlsx --replace-existing --db data/output/stats.db

run-all:  ## Run console script to parse all CSV files and export
	softball-stats --reparse-all --output data/output/stats.xlsx --db data/output/stats.db

clean:  ## Clean up generated files
	rm -rf dist/ build/ *.egg-info/
	rm -rf .coverage htmlcov/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

format:  ## Format Python code with Black and isort
	black src/ tests/ setup.py
	isort src/ tests/ setup.py

check-format:  ## Check if Python code is properly formatted
	black --check src/ tests/ setup.py
	isort --check-only src/ tests/ setup.py

lint:  ## Run all pre-commit checks (includes format and basic checks)
	pre-commit run --all-files

pre-commit-install:  ## Install pre-commit hooks
	pre-commit install

generate-test-data:  ## Generate fake test data CSV files in data/test/input/
	python scripts/generate_test_data.py

process-test-data:  ## Export test data to Excel file in data/test/ (requires generate-test-data first)
	python scripts/process_test_data.py

generate-and-process-test-data: generate-test-data process-test-data  ## Generate and export fake test data in one step
