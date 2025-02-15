VENV = venv
PYTHON = $(VENV)/bin/python
PIP = $(VENV)/bin/pip
REQUIREMENTS = requirements.txt
LOGS_DIR = logs

GREEN = \033[0;32m
NC = \033[0m # No Color

.PHONY: all setup clean run test lint help

all: help

help:
	@echo "Commands:"
	@echo "  make setup    - Create virtual environment and install dependencies"
	@echo "  make clean    - Remove virtual environment and cache"
	@echo "  make run      - Run the application"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Check code (ruff, pylint)"
	@echo "  make help     - Show this message"

setup: $(VENV)/bin/activate
	@echo "$(GREEN)>>> Installing dependencies...$(NC)"
	$(PIP) install -r $(REQUIREMENTS)
	@echo "$(GREEN)>>> Installation complete!$(NC)"

$(VENV)/bin/activate:
	@echo "$(GREEN)>>> Creating virtual environment...$(NC)"
	python3 -m venv $(VENV)
	@echo "$(GREEN)>>> Virtual environment created!$(NC)"

clean: cache
	@echo "$(GREEN)>>> Removing virtual environment...$(NC)"
	rm -rf $(VENV)
	rm -rf $(LOGS_DIR)
	@echo "$(GREEN)>>> Cleanup complete!$(NC)"

cache:
	@echo "$(GREEN)>>> Cleaning cache...$(NC)"
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type f -name "*.pyc" -delete
	@echo "$(GREEN)>>> Cache cleaned!$(NC)"

run:
	@echo "$(GREEN)>>> Running application...$(NC)"
	$(PYTHON) _main_.py

test:
	@echo "$(GREEN)>>> Running tests...$(NC)"
	$(PYTHON) -m pytest tests/

lint:
	@echo "$(GREEN)>>> Checking code...$(NC)"
	$(PYTHON) -m ruff check app/ --fix
	$(PYTHON) -m pylint app/