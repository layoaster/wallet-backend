"""
Data fixtures used to test API endpoints.
"""
from datetime import datetime
from decimal import Decimal

import pytest

from wallet_api.models import TransactionLog, TransactionType, User


@pytest.fixture
def user_view_init_data(db_session):
    """Add a set of user with initial balances."""
    # First user
    db_session.add(User(id=1, name="John Doe", email="john@email.com"))
    db_session.add(
        TransactionLog(
            user_id=1,
            trans_type=TransactionType.DEPOSIT,
            amount=Decimal("0.0"),
            opening_balance=Decimal("0.0"),
            new_balance=Decimal("0.0"),
            timestamp=datetime.utcnow(),
        )
    )

    # Second user
    db_session.add(User(id=2, name="Jane Doe", email="jane@email.com"))
    db_session.add(
        TransactionLog(
            user_id=2,
            trans_type=TransactionType.DEPOSIT,
            amount=Decimal("200.0"),
            opening_balance=Decimal("0.0"),
            new_balance=Decimal("200.0"),
            timestamp=datetime.utcnow(),
        )
    )

    db_session.commit()
