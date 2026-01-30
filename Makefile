# Makefile for softball-statistics

.PHONY: help setup install test run run-module clean format check-format lint pre-commit-install

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup:  ## Create and setup conda environment
	conda env create -f environment.yml
	@echo "Run: conda activate softball-stats"

install:  ## Install package in development mode (creates console script)
	pip install -e .

test:  ## Run all unit tests
	pytest tests/ -v --cov=src --cov-report=html

run:  ## Run console script (requires install first)
	softball-stats --file fray-cyclones-winter-01.csv --output data/output/stats.xlsx

run-module:  ## Run via python module (no install needed)
	python -m softball_statistics.cli --file fray-cyclones-winter-01.csv --output data/output/stats.xlsx

clean:  ## Clean up generated files
	rm -rf dist/ build/ *.egg-info/
	rm -rf .coverage htmlcov/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

format:  ## Format Python code with Black and isort
	source activate softball-stats && black src/ tests/ setup.py
	source activate softball-stats && isort src/ tests/ setup.py

check-format:  ## Check if Python code is properly formatted
	source activate softball-stats && black --check src/ tests/ setup.py
	source activate softball-stats && isort --check-only src/ tests/ setup.py

lint:  ## Run all pre-commit checks (includes format and basic checks)
	source activate softball-stats && pre-commit run --all-files

pre-commit-install:  ## Install pre-commit hooks
	source activate softball-stats && pre-commit install
