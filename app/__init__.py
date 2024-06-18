from datetime import timedelta

from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with your actual secret key
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=1)  # Set session lifetime to 1 day

    db.init_app(app)
    migrate.init_app(app, db)

    from app.routes import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    # If you have errors, register them here too
    # from app.errors import bp as errors_blueprint
    # app.register_blueprint(errors_blueprint)

    return app
