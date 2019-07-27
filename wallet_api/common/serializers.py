"""
Set of serializers for each API endpoint.
"""
from decimal import Context, Decimal, Inexact

from marshmallow import fields, Schema, ValidationError
from marshmallow.validate import Range


# Max number of decimal digits allowed
MAX_DECIMAL_PLACES = 2


# ---- Validators ---- #
def decimal_places(value: Decimal) -> bool:
    """
    Serializer validator that checks if `value` has no more than two decimal
    digits.

    :param value: a `Decimal` value (deserialized data).
    :return: `True` if validation passes. `False` otherwise.
    :raises marshmallow.exceptions.ValidationError: if validation fails.
    """
    try:
        value.quantize(Decimal(10) ** -MAX_DECIMAL_PLACES, context=Context(traps=[Inexact]))
    except Inexact:
        raise ValidationError(f"No more than {MAX_DECIMAL_PLACES} decimal digits allowed")

    return True


# ---- Serializers ---- #
class UserInputSchema(Schema):
    """
    Serializar of the user endpoint's request data.
    """

    #: User fullname.
    name = fields.Str(required=True, allow_none=False)
    #: User email.
    email = fields.Email(required=True, allow_none=False)
    #: Initial balance upon account creation.
    init_balance = fields.Decimal(
        missing=Decimal("0.00"), allow_none=False, as_string=True, validate=decimal_places
    )


class UserOutputSchema(Schema):
    """
    Serializar of the user endpoint's response data.
    """

    #: Id of the new user.
    id = fields.Int(dump_to="userId")


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
    toUserId = fields.Int(required=True, allow_none=False)
    #: Amount of money to tranfer.
    amount = fields.Decimal(
        required=True, allow_none=False, validate=(decimal_places, Range(min=0))
    )


class UserTransferOutputSchema(Schema):
    """
    Serializer of the user tranfer endpoint's response data.
    """

    #: Tranfer status.
    status = fields.Str()
    #: Transfer timestamp (UTC).
    timestamp = fields.DateTime()
