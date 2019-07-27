"""
Health set of endpoints.
"""
from flask import jsonify, Response
from flask_restful import Resource


class HealthLive(Resource):
    """
    Health probe: liveness.
    """

    def get(self) -> Response:
        """
        The application is considered to be alive as long as it can return
        a response.

        :return: Http (JSON) response with a status code of `200`.
        """
        return jsonify({"status": "OK"})
