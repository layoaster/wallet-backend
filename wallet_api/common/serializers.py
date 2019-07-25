"""
Set of serializers for each API endpoint.
"""
from marshmallow import fields, Schema


class UserBalanceOutputSchema(Schema):
    """
    Serializer of the user balance endpoint's response data.
    """

    #: User Id.
    userId = fields.Int()
    #: User current balance.
    balance = fields.Decimal(allow_none=False, as_string=True)


class UserTransferInputSchema(Schema):
    """
    Serializer of the user transfer endpoint's request data.
    """

    #: Transfer recipient user ID.
    toUserId = fields.Int(required=True)
    #: Amount of money to tranfer.
    amount = fields.Decimal(required=True)


class UserTransferOutputSchema(Schema):
    """
    Serializer of the user tranfer endpoint's response data.
    """

    #: Tranfer status.
    status = fields.Str()
    #: Transfer timestamp (UTC).
    timestamp = fields.DateTime()
