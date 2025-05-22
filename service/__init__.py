import sys
from flask import Flask
from flask_migrate import Migrate
from service import config
from service.common import log_handlers
from service.models import db  # import your db from models

# Create Flask app
app = Flask(__name__)
app.config.from_object(config)

# Initialize SQLAlchemy with app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Import routes and other modules after app and db init
from service import routes  # noqa: F401 E402
from service.common import error_handlers, cli_commands  # noqa: F401 E402

# Set up logging
log_handlers.init_logging(app, "gunicorn.error")

app.logger.info(70 * "*")
app.logger.info("  A C C O U N T   S E R V I C E   R U N N I N G  ".center(70, "*"))
app.logger.info(70 * "*")

try:
    with app.app_context():
        db.create_all()
except Exception as error:
    app.logger.critical("%s: Cannot continue", error)
    sys.exit(4)

app.logger.info("Service initialized!")

