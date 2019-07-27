"""
API custom exception classes.
"""
from typing import Union


class BaseApiException(Exception):
    """
    Base class for exceptions thrown by the API.
    """

    #: HTTP status code.
    status_code = 500
    #: Error message.
    message: Union[str, dict] = "Internal server error"
    #: Error mesage key for dict representation.
    prefix = "Error"

    def __init__(self, message: Union[str, dict] = None, status_code: int = None):
        # Exception.__init__(self)
        super().__init__()
        if message:
            self.message = message
        if status_code:
            self.status_code = status_code

    def to_dict(self) -> dict:
        """
        Dictionary representation of the exception.

        :return: Dictionary of errors adhering to the error schema.
        """
        rv = {self.prefix: self.message}
        return rv


class InvalidInputException(BaseApiException):
    """
    Exception raised when the request data is invalid.
    """

    status_code = 400
    prefix = "InputDataErrors"


class InvalidOutputException(BaseApiException):
    """
    Exception raised when the request data is invalid.
    """

    status_code = 500
    prefix = "OutputDataErrors"


class UserNotFoundException(BaseApiException):
    """
    Exception raised if an user is not found.
    """

    status_code = 403
    message = "User not found"


class UserExistException(BaseApiException):
    """
    Exception raised if an user already exists.
    """

    status_code = 403
    message = "User already exists"


class InsufficientFundsException(BaseApiException):
    """
    Exception raised if an user don't have enough funds to make a transfer.
    """

    status_code = 403
    message = "Insufficient funds"
