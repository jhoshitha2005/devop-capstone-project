"""
Package: service
Package for the application models and service routes
This module creates and configures the Flask app and sets up the logging and SQL database
"""

import sys
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from service import config
from service.common import log_handlers

# Initialize extensions (db and migrate will be initialized with app later)
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    """Create Flask app and initialize extensions"""
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Import routes and models after app creation to avoid circular imports
    from service import routes, models, error_handlers, cli_commands  # noqa: F401

    # Set up logging for production (example: gunicorn)
    log_handlers.init_logging(app, "gunicorn.error")

    app.logger.info(70 * "*")
    app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
    app.logger.info(70 * "*")

    with app.app_context():
        try:
            db.create_all()  # create tables
        except Exception as error:
            app.logger.critical("%s: Cannot continue", error)
            sys.exit(4)

    app.logger.info("Service initialized!")

    return app


# Create the app instance for flask CLI
app = create_app()
