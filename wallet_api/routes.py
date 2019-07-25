"""
App routes definitions.
"""
from flask import Blueprint
from flask_restful import Api

from wallet_api.resources.user import UserBalance, UserTransfer


# Application's blueprint
app_bp = Blueprint("app", __name__)

# Api plugin
api = Api(app_bp)


# User routes
api.add_resource(UserBalance, "/user/<int:user_id>/balance", endpoint="user_balance")
api.add_resource(UserTransfer, "/user/<int:user_id>/transfer", endpoint="user_transfer")
