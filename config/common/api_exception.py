from rest_framework.views import exception_handler
from rest_framework import exceptions
from rest_framework.response import Response

from common_library import response_serializer
from config.common.response_code import STATUS_RSP_INTERNAL_ERROR
from config.settings import logger


def cus_exception_handler(exc, context):
    print("ER|%s| %s" % (exc, context))
    logger.error(f"{exc}, {context}")

    response = exception_handler(exc, context)

    if response is not None:
        if isinstance(exc, exceptions.ParseError):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.AuthenticationFailed):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAuthenticated):
            code = response.status_code
            msg = "No Auth"
        elif isinstance(exc, exceptions.PermissionDenied):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotFound):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.MethodNotAllowed):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.NotAcceptable):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.UnsupportedMediaType):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.Throttled):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.ValidationError):
            code = response.status_code
            msg = exc.detail
        elif isinstance(exc, exceptions.APIException):
            code = exc.detail.get('code')
            msg = exc.detail.get(
                'message'
            )

            if exc.args[1:]:
                for key, val in exc.args[1].items():
                    response.data[key] = val

        else:
            code = response.status_code
            msg = "unknown error"

        response.status_code = 200
        response.data['code'] = code
        response.data['message'] = msg
        response.data['data'] = None

        try:
            del response.data['detail']
        except:
            pass

        return response
    else:
        return Response(response_serializer(STATUS_RSP_INTERNAL_ERROR), status=200)
