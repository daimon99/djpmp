# coding: utf-8
from django.http import Http404
from rest_framework import exceptions, status
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.response import Response
from rest_framework.views import set_rollback
import logging

log = logging.getLogger(__name__)


def exception_handler(exc, context):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's built-in `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, ValidationError):
        msg = '参数非法'
        data = {'msg': msg, 'code': -998, 'errors': exc.detail}
        set_rollback()
        return Response(data, status=status.HTTP_402_PAYMENT_REQUIRED)
    elif isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['Retry-After'] = '%d' % exc.wait

        if isinstance(exc.detail, (list, dict)):
            data = exc.detail
        else:
            data = exc.get_full_details()
        set_rollback()
        return Response(data, status=exc.status_code, headers=headers)
    elif isinstance(exc, Http404):
        msg = 'Not found.'
        data = {'msg': str(msg), 'code': -997}

        set_rollback()
        return Response(data, status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        msg = 'Permission denied.'
        data = {'msg': str(msg), 'code': -996}

        set_rollback()
        return Response(data, status=status.HTTP_403_FORBIDDEN)
    else:
        log.exception(exc)
        data = {
            'msg': '不能处理的异常',
            'code': -999
        }
        set_rollback()
        return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
