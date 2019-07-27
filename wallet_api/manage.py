"""
Flask CLI commands definition. To enable commands the following env-vars
must be set:
.. code-block:: shell

    FLASK_APP=wallet_api/manage.py
    FLASK_ENV=production
"""
from flask_migrate import Migrate

from wallet_api import create_app, db
from wallet_api.models import TransactionLog, User


app = create_app()
migrate = Migrate(app, db)


@app.shell_context_processor
def make_shell_context() -> dict:
    """The shell command."""
    return dict(app=app, db=db, User=User, TransactionLog=TransactionLog)


@app.cli.command("create_db")
def create_db() -> None:
    """Creates the entire database."""
    print("Creating application's tables ...")
    db.create_all()
    print("Tables created!!")
