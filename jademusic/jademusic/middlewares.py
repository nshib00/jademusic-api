from requests import Response
from rest_framework.exceptions import APIException


class ErrorHandlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwargs):
        try:
            response = self.get_response(request, *args, **kwargs)
        except APIException as exc:
            response = Response(data={'data': exc.detail}, status=exc.status_code)
        return response


