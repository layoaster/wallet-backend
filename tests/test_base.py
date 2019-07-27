"""
Set of tests for basic infra codebase.
"""
import pytest

from wallet_api import create_app
from wallet_api.config import FlaskAppConfig as app_conf
from wallet_api.config import PSQLClientConfig as db_conf


@pytest.mark.usefixtures("config_env_vars_setup")
class TestConfigFetch:
    """Test the env-vars fetcher class."""

    def test_string(self, config_class):
        """Test Value class."""
        assert isinstance(config_class.value, str)
        assert config_class.value == "test-value"

    def test_string_tuple(self, config_class):
        """Test TupleValue class."""
        assert isinstance(config_class.tuple_value, tuple)
        assert len(config_class.tuple_value) == 3
        assert "test-value2" in config_class.tuple_value

    def test_int(self, config_class):
        """Test IntValue class."""
        assert isinstance(config_class.int_value, int)
        assert config_class.int_value == 123456

    def test_int_tuple(self, config_class):
        """Test IntTupleValue class."""
        assert isinstance(config_class.int_tuple_value, tuple)
        assert len(config_class.int_tuple_value) == 6
        assert 5 in config_class.int_tuple_value
        assert isinstance(config_class.int_tuple_value[0], int)

    def test_float(self, config_class):
        """Test FloatValue class."""
        assert isinstance(config_class.float_value, float)
        assert config_class.float_value == 1.2

    def test_float_tuple(self, config_class):
        """Test FloatTupleValue class."""
        assert isinstance(config_class.float_tuple_value, tuple)
        assert len(config_class.float_tuple_value) == 6
        assert 3.3 in config_class.float_tuple_value
        assert isinstance(config_class.float_tuple_value[0], float)

    def test_boolean(self, config_class):
        """Test BooleanValue class."""
        assert isinstance(config_class.boolean_1, bool)
        assert isinstance(config_class.boolean_2, bool)
        assert isinstance(config_class.boolean_3, bool)
        assert isinstance(config_class.boolean_4, bool)
        assert config_class.boolean_1
        assert not config_class.boolean_2
        assert config_class.boolean_3
        assert not config_class.boolean_4

    def test_alternate_config_key(self, config_class):
        """Test custom config key for env-var."""
        assert config_class.another_conf == "test-alternate-key"

    def test_default_values(self, config_class):
        """Test default values for every type."""
        assert config_class.default_value == "default-test-value"
        assert "def-test-value2" in config_class.default_tuple_value
        assert config_class.default_int_value == 50
        assert 9 in config_class.default_int_tuple_value
        assert config_class.default_float_value == 20.6
        assert 8.8 in config_class.default_float_tuple_value
        assert not config_class.default_boolean

    def test_unexpected_tuple_value_type(self, config_class):
        """Test when a tuple-like env-var is set with incorrect value type."""
        assert isinstance(config_class.wrong_value_type, tuple)
        assert len(config_class.wrong_value_type) == 0

    def test_repr(self, config_class):
        """Test class __repr__ method."""
        representation = repr(config_class)
        assert "<Configuration" in representation
        assert config_class.__module__ in representation
        assert config_class.__name__ in representation
        assert "'>" in representation


class TestFlaskBase:
    """Test the Flask factory pattern and app's test client."""

    def test_config(self):
        """Test application factory configuration."""
        app = create_app()
        test_app = create_app(test=True)

        # Cheking testing config
        assert not app.testing
        assert test_app.testing
        assert app.secret_key == app_conf.secret_key
        assert test_app.secret_key != app_conf.secret_key

        # Checking database config
        assert app.config["SQLALCHEMY_DATABASE_URI"] == db_conf.connection_url()
        assert test_app.config["SQLALCHEMY_DATABASE_URI"] == db_conf.connection_url(test=True)
        assert app.config["SQLALCHEMY_DATABASE_URI"] != test_app.config["SQLALCHEMY_DATABASE_URI"]

    def test_client(self, client):
        """Test FLask's test client."""
        # Checking invalid path
        resp = client.get("/")
        assert resp.status_code == 404

        # Checking valid path
        resp = client.get("/health/live")
        assert resp.status_code == 200
