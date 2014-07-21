# -*- coding: utf-8 -*-

from django.core.exceptions import PermissionDenied
from django.http import Http404
from rest_framework import status, exceptions
from rest_framework.response import Response

from .serializers import CustomSerializer


def exception_handler(exc):
    """
    Returns the response that should be used for any given exception.

    By default we handle the REST framework `APIException`, and also
    Django's builtin `Http404` and `PermissionDenied` exceptions.

    Any unhandled exceptions may return `None`, which will cause a 500 error
    to be raised.
    """
    if isinstance(exc, exceptions.APIException):
        headers = {}
        if getattr(exc, 'auth_header', None):
            headers['WWW-Authenticate'] = exc.auth_header
        if getattr(exc, 'wait', None):
            headers['X-Throttle-Wait-Seconds'] = '%d' % exc.wait

        return Response({'error_code': CustomSerializer.get_api_code(exc.detail),
                         'error_message': exc.detail,
                         'errors': []},
                        status=exc.status_code,
                        headers=headers)

    elif isinstance(exc, Http404):
        return Response({'error_code': CustomSerializer.get_api_code('Not found'),
                         'error_message': 'Not found',
                         'errors': []},
                        status=status.HTTP_404_NOT_FOUND)

    elif isinstance(exc, PermissionDenied):
        return Response({'error_code': CustomSerializer.get_api_code('You do not have permission to perform this action.'),
                         'error_message': 'You do not have permission to perform this action.',
                         'errors': []},
                        status=status.HTTP_403_FORBIDDEN)

    # Note: Unhandled exceptions will raise a 500 error.
    return None