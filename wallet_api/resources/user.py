"""
User's set of endpoints.
"""
from decimal import Decimal

from flask import jsonify, request, Response
from flask_restful import Resource

from wallet_api.common.serializers import UserBalanceOutputSchema, UserTransferInputSchema
from wallet_api.common.utils import validation_error


class UserBalance(Resource):
    """
    API endpoint: User's balance.
    """

    def get(self, user_id: int) -> Response:
        """
        Fetch user's current balance.

        :param user_id: Id of the user to query for.
        :return: JSON response.
        """
        # TODO: perform actual DB data retrieval
        dump = UserBalanceOutputSchema().dump({"userId": 1, "balance": Decimal("300.45")})
        if not dump.errors:
            response = jsonify(dump.data)
        else:
            response = validation_error(dump.errors, status_code=500)

        return response


class UserTransfer(Resource):
    """
    API endpoint: User's money transfer.
    """

    def post(self, user_id: int) -> Response:
        """
        Transfer money between users.

        :param user_id: Sender user Id.
        :return: JSON response.
        """
        request_payload = UserTransferInputSchema().load(request.get_json(silent=True))
        if not request_payload.errors:
            deserialized_data = jsonify(request_payload.data)
        else:
            return validation_error(request_payload.errors)

        # TODO: perform actual DB data operation
        # TODO: return actual response (parse it with UserTransferOutputSchema)

        return deserialized_data
