# -*- coding: utf-8 -*-

import logging

from django.conf import settings


logger = logging.getLogger(__name__)


def get_api_code(message):
    """
    根据 message 获得相应的 API 错误代码

    """
    try:
        code = settings.API_ERROR_CODE[message]
    except KeyError:
        logger.error('API: System error when get the code of message "%(message)s"' % {'message': message})
        code = -1
    return code


def api_error_message(message):
    """
    通过 message 生成对应的标准出错信息

    """
    return {
        'error_message': message,
        'error_code': get_api_code(message),
        'errors': [],
    }