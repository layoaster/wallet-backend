"""
Data model definitions.
"""
import enum

from wallet_api import db


class TransactionType(enum.Enum):
    """
    Recognised transaction types.
    """

    TRANSFER_OUT = "transfer_out"
    TRANSFER_IN = "transfer_in"
    DEPOSIT = "deposit"
    CHARGE = "charge"
    WITHDRAWAL = "withdrawal"


# ---- DB Models  ---- #
class User(db.Model):
    """
    User data model.
    """

    __tablename__ = "user"

    #: Table's primary key.
    id = db.Column(db.Integer, primary_key=True)
    #: User fullname.
    name = db.Column(db.String(50), nullable=False)
    #: User transactions.
    transactions = db.relationship("TransactionLog", order_by="TransactionLog.timestamp", lazy=True)


class TransactionLog(db.Model):
    """
    Transaction logs data model.
    """

    __tablename__ = "transaction_log"

    #: Table's primary key.
    id = db.Column(db.Integer, primary_key=True)
    #: Transaction user.
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    #: Transaction type.
    trans_type = db.Column(db.Enum(TransactionType), nullable=False)
    #: Transaction amount.
    amount = db.Column(db.DECIMAL(scale=2), nullable=False)
    #: User opening balance (before the transanction).
    opening_balance = db.Column(db.DECIMAL(scale=2), nullable=False)
    #: User new balance (after the transanction).
    new_balance = db.Column(db.DECIMAL(scale=2), nullable=False)
    #: Transaction date-time.
    timestamp = db.Column(db.DateTime, nullable=False)
