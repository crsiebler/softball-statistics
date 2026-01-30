# Makefile for softball-statistics

.PHONY: help setup install test run run-module clean

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
	softball-stats --file fray-cyclones-winter-01.csv --output stats.xlsx

run-module:  ## Run via python module (no install needed)
	python -m softball_statistics.cli --file fray-cyclones-winter-01.csv --output stats.xlsx

clean:  ## Clean up generated files
	rm -rf dist/ build/ *.egg-info/
	rm -rf .coverage htmlcov/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +