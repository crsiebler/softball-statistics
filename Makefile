# Makefile for softball-statistics

.PHONY: help setup install test run run-all clean format check-format lint pre-commit-install

CONDA_BASE := $(shell conda info --base 2>/dev/null || echo /opt/anaconda3)
CONDA_PROFILE := $(CONDA_BASE)/etc/profile.d/conda.sh

FILE ?= data/input/fray-cyclones-winter-01_2026-01-29.csv

help:  ## Show this help message
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

setup:  ## Create conda environment (idempotent)
	conda env list | grep -q softball-stats || conda env create -f environment.yml

install:  ## Install package in development mode (creates console script)
	source $(CONDA_PROFILE) && conda activate softball-stats && pip install -e .

test:  ## Run all unit tests
	source $(CONDA_PROFILE) && conda activate softball-stats && pytest tests/ -v --cov=src --cov-report=html

run:  ## Run console script (requires install first)
	source $(CONDA_PROFILE) && conda activate softball-stats && softball-stats --file $(FILE) --output data/output/stats.xlsx --replace-existing

run-all:  ## Run console script to parse all CSV files and export
	source $(CONDA_PROFILE) && conda activate softball-stats && softball-stats --reparse-all --force --output data/output/stats.xlsx

clean:  ## Clean up generated files
	rm -rf dist/ build/ *.egg-info/
	rm -rf .coverage htmlcov/ .pytest_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +

format:  ## Format Python code with Black and isort
	source $(CONDA_PROFILE) && conda activate softball-stats && black src/ tests/ setup.py
	source $(CONDA_PROFILE) && conda activate softball-stats && isort src/ tests/ setup.py

check-format:  ## Check if Python code is properly formatted
	source $(CONDA_PROFILE) && conda activate softball-stats && black --check src/ tests/ setup.py
	source $(CONDA_PROFILE) && conda activate softball-stats && isort --check-only src/ tests/ setup.py

lint:  ## Run all pre-commit checks (includes format and basic checks)
	source $(CONDA_PROFILE) && conda activate softball-stats && pre-commit run --all-files

pre-commit-install:  ## Install pre-commit hooks
	source $(CONDA_PROFILE) && conda activate softball-stats && pre-commit install
