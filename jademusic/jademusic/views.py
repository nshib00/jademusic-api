from rest_framework.views import exception_handler

from audioparser.exceptions import http_exceptions


def api_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if response is not None:
        if exc.default_code == 'not_authenticated':
            response.status_code = 401
            response.data['detail'] = http_exceptions[401]
        else:
            response.status_code = 401
            response.data['detail'] = response.reason_phrase
        response.data['request_data'] = exc.default_detail
    return response
