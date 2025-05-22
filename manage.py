from service import app, db
from flask_migrate import Migrate
from flask.cli import FlaskGroup

migrate = Migrate(app, db)
cli = FlaskGroup(create_app=lambda: app)

if __name__ == "__main__":
    cli()
