PYTHON ?= python3
PORT ?= 8000
VENV_PYTHON := .venv/bin/python
MANAGE := $(VENV_PYTHON) manage.py

.DEFAULT_GOAL := help
.PHONY: help setup run shell createsuperuser makemigrations migrate showmigrations load-sample dump-sample check test verify

help: ## List the available commands
	@awk 'BEGIN {FS = ":.*## "} /^[a-z-]+:.*## / {printf "  make %-17s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: $(VENV_PYTHON) ## Create the virtual environment and install requirements
	$(VENV_PYTHON) -m pip install -r requirements.txt

$(VENV_PYTHON):
	$(PYTHON) -m venv .venv

run: ## Start the local development server (default PORT=8000)
	$(MANAGE) runserver 127.0.0.1:$(PORT)

shell: ## Open the Django shell
	$(MANAGE) shell

createsuperuser: ## Create a local admin account interactively
	$(MANAGE) createsuperuser

makemigrations: ## Generate migrations for catalog model changes
	$(MANAGE) makemigrations catalog

migrate: ## Apply pending migrations
	$(MANAGE) migrate

showmigrations: ## List migrations and their applied status
	$(MANAGE) showmigrations

load-sample: ## Load the sample catalog into a migrated database
	$(MANAGE) loaddata sample_catalog

dump-sample: ## Print the categories, tags, and products as fixture JSON
	@$(MANAGE) dumpdata catalog.Category catalog.Tag catalog.Product --indent 2

check: ## Run Django checks and detect missing migrations
	$(MANAGE) check
	$(MANAGE) makemigrations --check --dry-run

test: ## Run the Django test suite
	$(MANAGE) test

verify: check test ## Run all checks and tests
