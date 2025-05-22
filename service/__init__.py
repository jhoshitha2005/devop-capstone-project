import sys
from flask import Flask
from flask_migrate import Migrate
from service import config
from service.common import log_handlers

# Import your models.py which exposes `db`
from service import models

# Create Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize database
models.init_db(app)  # This should call db.init_app(app)

# Setup Flask-Migrate with app and db
migrate = Migrate(app, models.db)

# Import routes and others after app creation
from service import routes  # noqa: F401 E402
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Setup logging for production
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    # Create tables if needed
    models.init_db(app)
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")
