"""
Helpers for the API views.
"""
from flask import jsonify, Response


def validation_error(errors: dict, status_code: int = 400) -> Response:
    """
    Create a HTTP response with data validation errors.

    :param errors: A dict of the errors.
    :param status_code: Status code of the HTTP response.
    """
    response = jsonify({"fieldErrors": errors})
    response.status_code = status_code

    return response
