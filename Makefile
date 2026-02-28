.PHONY: help install validate codegen codegen-python codegen-ts check-codegen \
       lint lint-py lint-ts format format-py format-ts format-check format-check-py format-check-ts \
       typecheck typecheck-py typecheck-ts test test-py test-ts build build-py build-ts check clean

help: ## Show available targets with descriptions
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install Python and Node dependencies
	pip install -e ".[sdk,dev]"
	npm install

# --- Schema Validation ---

validate: ## Validate all JSON Schema files
	@echo "Validating JSON schemas..."
	@for f in contracts/schemas/*.json; do \
		check-jsonschema --check-metaschema "$$f" && echo "  ✓ $$f" || exit 1; \
	done
	@echo "All schemas valid."

# --- Codegen ---

codegen: codegen-python codegen-ts ## Run all codegen (Python + TypeScript)

codegen-python: ## Generate Pydantic models from JSON schemas
	$(PYTHON) codegen/generate_python.py

codegen-ts: ## Generate TypeScript interfaces from JSON schemas
	node codegen/generate_typescript.mjs

check-codegen: codegen ## Verify generated code matches schemas (CI)
	@git diff --exit-code generated/ || \
		(echo "ERROR: Generated code is out of date. Run 'make codegen' and commit." && exit 1)

# --- Linting ---

lint: lint-py lint-ts ## Lint Python + TypeScript

lint-py: ## Lint Python code
	ruff check generated/python/ sdk/python/ tests/python/

lint-ts: ## Lint TypeScript code
	npm run lint

# --- Formatting ---

format: format-py format-ts ## Format Python + TypeScript

format-py: ## Format Python code
	ruff format generated/python/ sdk/python/ tests/python/
	ruff check --fix generated/python/ sdk/python/ tests/python/

format-ts: ## Format TypeScript code
	npm run format

format-check: format-check-py format-check-ts ## Check formatting without modifying

format-check-py: ## Check Python formatting
	ruff format --check generated/python/ sdk/python/ tests/python/

format-check-ts: ## Check TypeScript formatting
	npm run format:check

# --- Type checking ---

typecheck: typecheck-py typecheck-ts ## Typecheck Python + TypeScript

typecheck-py: ## Typecheck Python (mypy)
	mypy generated/python/ sdk/python/

typecheck-ts: ## Typecheck TypeScript (tsc)
	npm run typecheck

# --- Testing ---

test: test-py test-ts ## Run all tests

test-py: ## Run Python tests
	pytest tests/python/ -m unit -v

test-ts: ## Run TypeScript tests
	npm run test

# --- Build ---

build: build-py build-ts ## Build all distributable packages

PYTHON ?= python3

build-py: ## Build Python wheel and sdist
	$(PYTHON) -m build
	@echo "Verifying Python package..."
	@pip install --quiet dist/*.whl 2>/dev/null || pip3 install --quiet dist/*.whl
	@$(PYTHON) -c "from cowork_platform import ToolRequest; print('  Python package OK')"
	@$(PYTHON) -c "from cowork_platform_sdk import CoworkAPIError; print('  Python SDK OK')"

build-ts: ## Compile TypeScript to dist/
	npx tsc

# --- CI Gate ---

check: validate check-codegen lint format-check typecheck test ## CI gate: full check

# --- Clean ---

clean: ## Remove generated artifacts and caches
	rm -rf dist/ build/ *.egg-info .mypy_cache .pytest_cache .ruff_cache
	rm -rf node_modules/.cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
