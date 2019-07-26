"""
User's set of endpoints.
"""
from datetime import datetime
from decimal import Decimal

from flask import jsonify, request, Response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from wallet_api import db
from wallet_api.common.serializers import (
    UserBalanceOutputSchema,
    UserInputSchema,
    UserOutputSchema,
    UserTransferInputSchema,
)
from wallet_api.common.utils import validation_error
from wallet_api.models import TransactionLog, TransactionType, User


class UserResource(Resource):
    """
    API endpoint: user resource.
    """

    def post(self) -> Response:
        """
        Creates a new user. Aditionally, initialize the transaction log to
        store a initial balance.

        :return: JSON response.
        """
        request_payload = UserInputSchema().load(request.get_json(silent=True))
        if not request_payload.errors:
            deserialized_data = request_payload.data
        else:
            return validation_error(request_payload.errors)

        # Insert user data
        new_user = User(name=deserialized_data["name"], email=deserialized_data["email"])
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()

            response = jsonify({"error": "User already exists."})
            response.status_code = 403
        else:
            # Insert initial transaction entry.
            init_balance = TransactionLog(
                user_id=new_user.id,
                trans_type=TransactionType.DEPOSIT,
                amount=deserialized_data["init_balance"],
                opening_balance=deserialized_data["init_balance"],
                new_balance=deserialized_data["init_balance"],
                timestamp=datetime.utcnow(),
            )
            db.session.add(init_balance)
            db.session.commit()

            response = jsonify(UserOutputSchema().dump(new_user.__dict__).data)
            response.status_code = 201

        return response


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
