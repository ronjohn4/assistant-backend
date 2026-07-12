# Agent Orchestrator

This project provides a lightweight web-based chat interface for interacting with an orchestrator-style assistant. The app is designed to receive user messages, coordinate backend agent logic, and return responses through a simple Flask UI.

## What this project does

- Presents a chat experience in the browser through a Flask app.
- Routes user requests to the orchestration layer and supporting tools.
- Supports helper capabilities such as general knowledge, weather, and date/time lookups.
- Serves the interface from the templates and static folders under the app package.

## Project structure

- app/ - Flask application package and route logic
- app/api/ - API/tool modules used by the orchestrator
- app/templates/ - HTML templates for the user interface
- app/static/ - CSS and other frontend assets
- main.py - entry point for running the application

## How to set up the project

1. Make sure Python 3.11 or newer is installed.
2. Create and activate a virtual environment:
   - Windows:
     - `python -m venv .venv`
     - `.venv\Scripts\activate`
3. Install the project dependencies:
   - `pip install -e .`

## How to run the project

Start the app with:

- `python main.py`

By default, the app runs on port 5010. You can open it in your browser at:

- `http://localhost:5010`

To run in debug mode, set:

- `set FLASK_DEBUG=1`
- `python main.py`

## How to manage the project

- Update dependencies when needed by running `pip install -e .` again after changing project requirements.
- If you add or modify Python modules, restart the Flask server so the latest code is loaded.
- Keep environment variables in a `.env` file when needed; the app loads environment settings automatically.
- For local development, it is helpful to review the logs in the terminal when troubleshooting issues.

## Notes

This project is intentionally simple and focused on the interaction layer between the human user and the orchestrator agent.
