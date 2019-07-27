"""
Pytest's fixtures.
"""
import os

import pytest
from flask_migrate import downgrade, Migrate, upgrade

from wallet_api import create_app
from wallet_api import db as _db
from wallet_api.common.configfetch import (
    BooleanValue,
    Configuration,
    FloatTupleValue,
    FloatValue,
    IntTupleValue,
    IntValue,
    TupleValue,
    Value,
)


ALEMBIC_CONFIG_FILE = "./migrations/alembic.ini"


@pytest.fixture(scope="session")
def app():
    """Flask application for tests."""
    app = create_app(test=True)

    # setUp
    ctx = app.app_context()
    ctx.push()

    yield app

    # tearDown
    ctx.pop()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture(scope="session")
def db(app):
    """Session-wide test database."""
    _db.app = app

    # Apply migrations (creating tables)
    Migrate(app, _db)
    upgrade(revision="head")

    yield _db

    # Undo migrations (removing tables)
    downgrade(revision="base")


@pytest.fixture(scope="function")
def db_session(db):
    """
    Database session as a fixture to isolate test from each other. Basically,
    test units get wrapped in database transactions that always get rolled back.
    """
    # Start a transaction
    connection = db.engine.connect()
    transaction = connection.begin()

    # Bind a session to the transaction. The empty `binds` dict is necessary
    # when specifying a `bind` option, or else Flask-SQLAlchemy won't scope
    # the connection properly
    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    # Make sure the session, connection, and transaction can't be closed
    # by accident in the codebase
    connection.force_close = connection.close
    transaction.force_rollback = transaction.rollback

    connection.close = lambda: None
    transaction.rollback = lambda: None
    session.close = lambda: None

    db.session = session

    yield session

    session.remove()
    transaction.force_rollback()
    connection.force_close()


# ----- Fixtures to test config via env-vars infra ----- #
@pytest.fixture
def config_env_vars_setup():
    """Sets environment vars necessary to test."""
    # Value
    os.environ["TEST_SAMPLE_VALUE"] = "test-value"
    # TupleValue
    os.environ["TEST_SAMPLE_TUPLE_VALUE"] = "test-value1,test-value2,test-value3"
    # IntValue
    os.environ["TEST_SAMPLE_INT_VALUE"] = "123456"
    # IntTupleValue
    os.environ["TEST_SAMPLE_INT_TUPLE_VALUE"] = "1,2,3,4,5,6"
    # FloatValue
    os.environ["TEST_SAMPLE_FLOAT_VALUE"] = "1.2"
    # FloatTupleValue
    os.environ["TEST_SAMPLE_FLOAT_TUPLE_VALUE"] = "1.1,2.2,3.3,4.4,5.5,6"
    # BooleanValue 1
    os.environ["TEST_SAMPLE_BOOLEAN_1"] = "true"
    # BooleanValue 2
    os.environ["TEST_SAMPLE_BOOLEAN_2"] = "0"
    # BooleanValue 3
    os.environ["TEST_SAMPLE_BOOLEAN_3"] = "y"
    # BooleanValue 4
    os.environ["TEST_SAMPLE_BOOLEAN_4"] = "no"
    # Alternate config key
    os.environ["TEST_ALTERNATE_CONF"] = "test-alternate-key"
    # Incorrect tuple-like value type
    os.environ["TEST_SAMPLE_WRONG_VALUE_TYPE"] = "test1,test2"


@pytest.fixture
def config_class():
    class TestConfig(Configuration):
        _prefix = "TEST_SAMPLE_"

        # Value
        value = Value()
        # TupleValue
        tuple_value = TupleValue()
        # IntValue
        int_value = IntValue()
        # IntTupleValue
        int_tuple_value = IntTupleValue()
        # FloatValue
        float_value = FloatValue()
        # FloatTupleValue
        float_tuple_value = FloatTupleValue()
        # BooleanValue 1
        boolean_1 = BooleanValue()
        # BooleanValue 2
        boolean_2 = BooleanValue()
        # BooleanValue 3
        boolean_3 = BooleanValue()
        # BooleanValue 4
        boolean_4 = BooleanValue()
        # Alternate config key
        another_conf = Value(alternate_key="TEST_ALTERNATE_CONF")
        # Default values
        default_value = Value("default-test-value")
        default_tuple_value = TupleValue(("def-test-value1", "def-test-value2"))
        default_int_value = IntValue(50)
        default_int_tuple_value = IntTupleValue((7, 8, 9))
        default_float_value = FloatValue(20.6)
        default_float_tuple_value = FloatTupleValue((7.7, 8.8, 9.9))
        default_boolean = BooleanValue(False)
        # Incorrect tuple-like value type
        wrong_value_type = IntTupleValue()

    return TestConfig
