"""Application configuration."""
import os
from pathlib import Path


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    ORCHESTRATOR_MODEL = os.environ.get("ORCHESTRATOR_MODEL", "claude-sonnet-5")
    PORT = os.environ.get("PORT") or "5010"
    FLASK_DEBUG = int(os.environ.get("FLASK_DEBUG", 0))
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")

    LANGSMITH_API_KEY = os.environ.get("LANGSMITH_API_KEY")
    LANGSMITH_TRACING = os.environ.get("LANGSMITH_TRACING")
    LANGSMITH_PROJECT = os.environ.get("LANGSMITH_PROJECT")
