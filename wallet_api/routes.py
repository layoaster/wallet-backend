"""
App routes definitions.
"""
from flask import Blueprint, jsonify, Response
from flask_restful import Api

from wallet_api.common.exception import BaseApiException
from wallet_api.resources.user import UserBalance, UserResource, UserTransfer


# Application's blueprint
app_bp = Blueprint("app", __name__)

# Api plugin
api = Api(app_bp)


# ----- User routes ----- #
api.add_resource(UserResource, "/user", endpoint="user")
api.add_resource(UserBalance, "/user/<int:user_id>/balance", endpoint="user_balance")
api.add_resource(UserTransfer, "/user/<int:user_id>/transfer", endpoint="user_transfer")


# ----- App exceptions handler ----- #
@app_bp.errorhandler(Exception)
def handle_base_exceptions(e: Exception) -> Response:
    """
    API custom exceptions handler.

    :param e: Exception raised in the application.
    :return: JSON response with proper error message.
    """
    if isinstance(e, BaseApiException):
        # API custom exception
        response = jsonify(e.to_dict())
        response.status_code = e.status_code
    else:
        raise e

    return response
