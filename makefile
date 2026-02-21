.PHONY: install sync lock add dev api langgraph-dev langgraph-up langgraph-build help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'


# ── FastAPI ───────────────────────────────────────────────────────────

api: ## Run FastAPI dev server with hot reload
	uv run fastapi dev api.py

api-prod: ## Run FastAPI in production mode
	uv run fastapi run api.py

# ── LangGraph CLI ─────────────────────────────────────────────────────

langgraph-dev: ## Run LangGraph dev server (in-memory, with Studio UI)
	uv run langgraph dev

langgraph-up: ## Start LangGraph server
	uv run langgraph up

# langgraph-build: ## Build the LangGraph Docker image
# 	uv run langgraph build

# langgraph-test: ## Run LangGraph graph verification
# 	uv run langgraph-verify-graphs

# ── Run scripts ───────────────────────────────────────────────────────

run: ## Run main.py
	uv run python main.py
