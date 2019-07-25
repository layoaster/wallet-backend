"""
Environment variables configuration fetcher class-level support.
"""
import os


class Value(object):
    """
    Defines a value that has to be potentially fetched from the variable
    environment.
    """

    def __init__(self, default_value=None, prefix=None, alternate_key=None):
        """
        Initializes a class instance.

        :param default_value: A default value in case the variable cannot be
            found in the environment.
        :type default_value: object
        :param prefix: The prefix for the environment variable.
        :type prefix: str
        :param alternate_key: The alternate key where to search for this
            variable in the environment.
        :type alternate_key: str
        """
        self.default_value = default_value
        self.prefix = prefix
        self.alternate_key = alternate_key

    def get_value_from_env(self, key):
        """
        Fetches the actual value from the variable environment.

        :param key: The key in the configuration class. To be ignored if
            `alternate_key` was defined at initialization level.
        :type key: str
        :returns: The actual value.
        :rtype: object
        """
        if self.alternate_key:
            key = self.alternate_key
        else:
            key = "{}{}".format(self.prefix or "", key)
        return os.environ.get(key.upper()) or self.default_value


class TupleValue(Value):
    """
    Extends the :class:`Value` class to return the environment variable value
    as a tuple of str.
    """

    #: The type to cast to
    _type = str

    def __init__(self, default_value=None, prefix=None, alternate_key=None, separator=","):
        """
        Initializes a class instance.

        :param default_value: A default value in case the variable cannot be
            found in the environment.
        :type default_value: object
        :param prefix: The prefix for the environment variable.
        :type prefix: str
        :param alternate_key: The alternate key where to search for this variable
            in the environment.
        :type alternate_key: str
        """
        super().__init__(default_value, prefix, alternate_key)
        self.separator = separator

    def get_value_from_env(self, key):
        """
        Fetches the actual value from the variable environment as a tuple of str.

        :param key: The key in the configuration class. To be ignored if
            `alternate_key` was defined at initialization level.
        :type key: str
        :returns: The actual value.
        :rtype: tuple
        """
        val = super().get_value_from_env(key) or ()
        if isinstance(val, tuple):
            return val
        else:
            try:
                return tuple(self._type(v) for v in val.split(self.separator))
            except (AttributeError, ValueError):
                return ()


class IntTupleValue(TupleValue):
    """
    Extends the :class:`TupleValue` class to return the environment variable
    value as a tuple of int.
    """

    #: The type to cast to
    _type = int


class FloatTupleValue(TupleValue):
    """
    Extends the :class:`TupleValue` class to return the environment variable
    value as a tuple of float.
    """

    #: The type to cast to
    _type = float


class BooleanValue(Value):
    """
    Extends the :class:`Value` class to return the environment variable value
    as a coerced boolean.
    """

    def get_value_from_env(self, key):
        """
        Fetches the actual value from the variable environment as a boolean.

        :param key: The key in the configuration class. To be ignored if
                    `alternate_key` was defined at initialization level.
        :type key: str
        :returns: The actual value.
        :rtype: bool
        """
        val = super().get_value_from_env(key) or ""
        if isinstance(val, bool):
            return val
        else:
            val = val.lower()
        if val in ("true", "1", "y", "yes"):
            return True
        if val in ("false", "0", "n", "no"):
            return False


class IntValue(Value):
    """
    Extends the :class:`Value` class to return the environment variable value
    as a coerced int.
    """

    #: The type to cast to
    _type = int

    def get_value_from_env(self, key):
        """
        Fetches the actual value from the variable environment as the type
        specified in `_type`.

        :param key: The key in the configuration class. To be ignored if
                    `alternate_key` was defined at initialization level.
        :type key: str
        :returns: The actual value.
        :rtype: type
        """
        val = super().get_value_from_env(key) or ""
        if isinstance(val, self._type):
            return val
        else:
            try:
                return self._type(val)
            except ValueError:
                return self._type(0)


class FloatValue(IntValue):
    """
    Extends the :class:`IntValue` class to return the environment variable value
    as a coerced float.
    """

    #: The type to cast to
    _type = float


def get_attributes(obj):
    """
    Fetches the attributes from an object.

    :param obj: The object.
    :type obj: object
    :returns: A dictionary of attributes and their values from the object.
    :rtype: dict
    """
    return {k: getattr(obj, k) for k in dir(obj) if not k.startswith("__")}


class ConfigurationBase(type):
    """
    The configuration base metaclass.

    This also allows to specify a prefix as a `_prefix` property at the
    class level definition.
    """

    def __new__(cls, name, bases, attrs):
        """
        Invoked at creation level to scroll through the attributes and process them
        (also for parent classes).
        """
        parents = [base for base in bases if isinstance(base, ConfigurationBase)]
        settings_vars = {}
        if parents:
            for base in bases[::-1]:
                settings_vars.update(get_attributes(base))
        attrs = dict(settings_vars, **attrs)

        # we fetch the actual values from environment here
        prefix = attrs.pop("_prefix", None)
        for (key, val) in attrs.items():
            if isinstance(val, Value):
                val.prefix = prefix
                attrs[key] = val.get_value_from_env(key)

        return super(ConfigurationBase, cls).__new__(cls, name, bases, attrs)

    def __repr__(self):
        return "<Configuration '{0}.{1}'>".format(self.__module__, self.__name__)


class Configuration(object, metaclass=ConfigurationBase):
    """
    The base configuration class (invoked on top of metaclass :class:`ConfigurationBase`).
    """
