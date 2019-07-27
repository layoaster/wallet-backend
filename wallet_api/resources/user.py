"""
User's set of endpoints.
"""
from datetime import datetime

from flask import jsonify, request, Response
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound

from wallet_api import db
from wallet_api.common import exception
from wallet_api.common.serializers import (
    UserBalanceOutputSchema,
    UserInputSchema,
    UserOutputSchema,
    UserTransferInputSchema,
    UserTransferOutputSchema,
)
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
        if request_payload.errors:
            raise exception.InvalidInputException(request_payload.errors)
        req_data = request_payload.data

        # Insert user data
        new_user = User(name=req_data["name"], email=req_data["email"])
        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise exception.UserExistException
        else:
            # Insert initial transaction entry.
            init_balance = TransactionLog(
                user_id=new_user.id,
                trans_type=TransactionType.DEPOSIT,
                amount=req_data["init_balance"],
                opening_balance=req_data["init_balance"],
                new_balance=req_data["init_balance"],
                timestamp=datetime.utcnow(),
            )
            db.session.add(init_balance)
            db.session.commit()

            db.session.refresh(new_user)
            serialized_resp = UserOutputSchema().dump(new_user.__dict__)
            if serialized_resp.errors:
                raise exception.InvalidOutputException(serialized_resp.errors)

            response = jsonify(serialized_resp.data)
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
        try:
            user = User.query.filter_by(id=user_id).one()
        except NoResultFound:
            raise exception.UserNotFoundException

        serialized_resp = UserBalanceOutputSchema().dump(
            {"userId": user.id, "balance": user.transactions[-1].new_balance}
        )
        if serialized_resp.errors:
            raise exception.InvalidOutputException(serialized_resp.errors)

        return jsonify(serialized_resp.data)


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
        if request_payload.errors:
            raise exception.InvalidInputException(request_payload.errors)
        req_data = request_payload.data

        try:
            sender = User.query.filter_by(id=user_id).one()
            recipient = User.query.filter_by(id=req_data["toUserId"]).one()
        except NoResultFound:
            raise exception.UserNotFoundException

        # Check funds
        if req_data["amount"] > sender.transactions[-1].new_balance:
            raise exception.InsufficientFundsException

        timestamp = datetime.utcnow()

        # Users new balance
        sender_new_balance = sender.transactions[-1].new_balance - req_data["amount"]
        recipient_new_balance = recipient.transactions[-1].new_balance + req_data["amount"]

        # A transfer creates two rows (sender, recipient)
        db.session.add(
            TransactionLog(
                user_id=sender.id,
                trans_type=TransactionType.TRANSFER_OUT,
                amount=req_data["amount"],
                opening_balance=sender.transactions[-1].new_balance,
                new_balance=sender_new_balance,
                timestamp=timestamp,
            )
        )
        db.session.add(
            TransactionLog(
                user_id=recipient.id,
                trans_type=TransactionType.TRANSFER_IN,
                amount=req_data["amount"],
                opening_balance=recipient.transactions[-1].new_balance,
                new_balance=recipient_new_balance,
                timestamp=timestamp,
            )
        )

        try:
            db.session.commit()
        except SQLAlchemyError:
            db.session.rollback()
            # TODO: Log exception
            serialized_resp = UserTransferOutputSchema().dump(
                {"status": "failed", "timestamp": timestamp}
            )
        else:
            serialized_resp = UserTransferOutputSchema().dump(
                {"status": "done", "timestamp": timestamp}
            )
        finally:
            db.session.close()

        if serialized_resp.errors:
            raise exception.InvalidOutputException(serialized_resp.errors)
        return jsonify(serialized_resp.data)
