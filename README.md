# Agent Orchestrator

This project provides a lightweight Flask backend for an orchestrator-style assistant. It accepts user queries, routes them through a LangGraph-based orchestration flow, and can call built-in tools such as date/time lookup, weather lookup, and web search.

## What this project does

- Exposes a small REST API for sending prompts to the orchestrator.
- Routes requests through an LLM-backed agent workflow with tool support.
- Includes helper capabilities for date/time, weather, and web search lookups.
- Writes logs to stdout or a rotating log file under the logs directory.

## Project structure

- app/ - Flask application package
- app/api/ - API route definitions and blueprint registration
- app/tools/ - orchestrator logic and tool implementations
- main.py - application entry point
- logs/ - runtime log output
- pyproject.toml - project metadata and dependencies

## Prerequisites

- Python 3.11 or newer
- An Anthropic API key for the orchestrator model

## Setup

1. Create and activate a virtual environment:
   - Windows:
     - `python -m venv .venv`
     - `.venv\Scripts\activate`
2. Install the project dependencies:
   - `pip install -e .`
3. Copy the sample environment file and update it:
   - `copy .env_example .env`
   - Fill in your API key and model settings

## Configuration

The app loads environment variables from a `.env` file. The main settings are:

- `SECRET_KEY` - Flask secret key
- `PORT` - HTTP port to listen on (defaults to `5002` if unset)
- `FLASK_DEBUG` - set to `1` for debug mode
- `ORCHESTRATOR_MODEL` - model name for the orchestrator
- `ANTHROPIC_API_KEY` - Anthropic API credential
- `LOG_TO_STDOUT` - write logs to stdout when set to `true`
- `LOG_LEVEL` - logging level such as `DEBUG`, `INFO`, or `ERROR`

Optional LangSmith tracing settings are also supported:

- `LANGSMITH_API_KEY`
- `LANGSMITH_TRACING`
- `LANGSMITH_PROJECT`

## Running the app

Start the backend with:

- `python main.py`

The app will listen on the configured port. If `PORT` is not set, it defaults to `5002`.

## API endpoints

- `GET /health` - returns a simple health status payload
- `POST /agent` - sends a prompt to the orchestrator

Example request:

```bash
curl -X POST http://localhost:5002/agent -H "Content-Type: application/json" -d "{\"query\":\"What time is it?\"}"
```

## Development notes

- Restart the Flask server after changing Python modules.
- Review the logs in the terminal or the `logs/` directory when troubleshooting.
- New tools can be added under `app/tools/` and wired into the orchestrator in `app/tools/orchestrator.py`.
