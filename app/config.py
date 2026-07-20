"""Application configuration."""
import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ORCHESTRATOR_MODEL = os.environ.get("ORCHESTRATOR_MODEL")
    PORT = os.environ.get("PORT")
    FLASK_DEBUG = int(os.environ.get("FLASK_DEBUG"))
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT").lower() == "true"
    LOG_LEVEL = os.environ.get("LOG_LEVEL")

    LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
    LANGSMITH_TRACING = os.environ.get("LANGSMITH_TRACING")
    LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT")
