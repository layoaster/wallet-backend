"""
WSGI application entrypoint/runner.
"""
from wallet_api import create_app

# Obtains an app instance
app = create_app()

if __name__ == "__main__":
    app.run()
