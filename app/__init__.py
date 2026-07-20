"""Flask application factory."""
from flask import Flask
from flask_restful import Api
import os
import logging
from logging.handlers import SMTPHandler, RotatingFileHandler

from app.config import Config

flask_api = Api()

def create_app(config_object=Config) -> Flask:
    app = Flask(__name__)
    app.config.from_object(config_object)

    from app.api import bp as api_bp
    flask_api.init_app(api_bp)
    app.register_blueprint(api_bp)

    app.logger.handlers = []  # remove the default logger to StreamHandler()
    if app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/assistant-backend.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s '
            '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(app.config['LOG_LEVEL'])
        app.logger.addHandler(file_handler)

    app.logger.setLevel(app.config['LOG_LEVEL'])
    app.logger.info('Assistant backend startup')

    return app

app = create_app()
