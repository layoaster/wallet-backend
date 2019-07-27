import logging
import os
from functools import wraps

from flask import current_app, Flask
from flask_sqlalchemy import SQLAlchemy

from wallet_api.config import FlaskAppConfig as flask_conf
from wallet_api.config import PSQLClientConfig as db_conf


db = SQLAlchemy()


def create_app(test: bool = False) -> Flask:
    """
    Application factory pattern - Creates and initialize the application.

    :param test: `True` to return an application for unit-testing.
    :return: Flask's application object.
    """
    app = Flask(__name__)

    # Flask config flags
    app.config.from_mapping(  # type: ignore
        {
            "SECRET_KEY": flask_conf.secret_key,
            # SQLAlchemy specific settings
            "SQLALCHEMY_DATABASE_URI": db_conf.connection_url(),
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        }
    )
    if test:
        app.config.from_mapping(
            {
                "SECRET_KEY": os.urandom(16),
                "TESTING": True,
                "SQLALCHEMY_DATABASE_URI": db_conf.connection_url(test=True),
            }
        )

    # Logging config
    app.logger.setLevel(logging.DEBUG if app.config["DEBUG"] else logging.INFO)

    # Initializes database
    db.init_app(app)

    # Registering blueprints
    from wallet_api.routes import app_bp

    app.register_blueprint(app_bp)

    return app


# ---- Flask views decorator ---- #
def db_isolation_level(level: str):
    """
    Flask view decorator to set SQLAlchemy transaction isolation level.
    https://docs.sqlalchemy.org/en/13/dialects/postgresql.html#postgresql-isolation-level

    :param level: SQLAlchemy driver-specific isolation level.
    :return: decorated view funcion.
    """

    def decorator(view):
        @wraps(view)
        def view_wrapper(*args, **kwargs):
            if not current_app.config["TESTING"]:
                db.session.connection(execution_options={"isolation_level": level})
            return view(*args, **kwargs)

        return view_wrapper

    return decorator
