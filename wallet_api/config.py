"""
Configuration classes of the application.
"""
from wallet_api.common.configfetch import Configuration, IntValue, Value


class FlaskAppConfig(Configuration):
    """
    Configuration class of the Flask framework. More info:
    http://flask.pocoo.org/docs/1.0/config/#builtin-configuration-values
    """

    #: Environment variables prefix of the class.
    _prefix = "FLASK_"

    #: Flask environment (production, development).
    # In `development` automatically enables `DEBUG` mode which subsequently
    # enables `PROPAGATE_EXCEPTIONS` and `PRESERVE_CONTEXT_ON_EXCEPTION`
    # sets http://flask.pocoo.org/docs/1.0/config/#builtin-configuration-values
    env = Value("production")

    #: Flask secret key
    secret_key = Value("")


class PSQLClientConfig(Configuration):
    """Configuration class of the PostgreSQL client."""

    #: Environment variables prefix of the class.
    _prefix = "PSQL_CLIENT_"

    #: PostgreSQL sever host.
    host = Value("localhost")

    #: PostgreSQL sever port.
    port = IntValue(5432)

    #: PostgreSQL sever dialect.
    dialect = Value("postgresql+psycopg2")

    #: PostgreSQL database.
    database = Value("wallet_api")

    #: Database used for unittesting.
    test_database = Value("wallet_api_test")

    #: PostgreSQL db username.
    username = Value("db_admin")

    #: PostgreSQL db password.
    password = Value("")

    @staticmethod
    def connection_url(test: bool = False) -> str:
        """
        Gets the database connection URL as expected by SQLAlchemy.
        https://docs.sqlalchemy.org/en/latest/core/engines.html#postgresql

        :param test: If `True` returns the URL of the testing database.
        :return: Corresponding PostgreSQL connection URL.
        """
        base_url = "{}://{}:{}@{}:{}/{}".format(
            PSQLClientConfig.dialect,
            PSQLClientConfig.username,
            PSQLClientConfig.password,
            PSQLClientConfig.host,
            PSQLClientConfig.port,
            PSQLClientConfig.test_database if test else PSQLClientConfig.database,
        )

        return base_url
