# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from rest_framework.response import Response
from rest_framework import status


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


def api_success_message(addition=None):
    """
    生成对应的标准 API 成功信息 (仅限于为前端提供, 客户端不考虑在内)

    :param addition: 在成功信息中添加额外的附加信息, 该参数为 dict 类型, 会直接嵌入成功信息中, 不会进行嵌套
    :return: 标准的 API 成功信息 dict
    """

    message = {
        'error_code': 0
    }
    if addition:
        message = dict(message, **addition)
    return message


def api_error_message(message):
    """
    通过 message 生成对应的标准 API 出错信息

    """
    return {
        'error_message': message,
        'error_code': get_api_code(message),
        'errors': [],
    }


def process_errors(errors):
    """
    将 Django 生成的错误(Django 的 form.errors, django-rest-framework 的 serializers.errors) 转换为标准的 API 错误输出

    与 api_error_message 不同的是 process_errors 用于处理验证类错误, 返回内容中包含各个字段的验证错误信息,
    api_error_message 用于处理非验证类错误, 返回内容只包含单独的错误信息

    :param errors: 错误信息
    :return: 标准的API错误信息dict
    """
    new_errors = {
        'errors': [],
    }

    for key, value in errors.items():
        if key == 'non_field_errors':
            new_errors['error_code'] = get_api_code(value[0])
            new_errors['error_message'] = value[0]
        else:
            new_errors['errors'].append({
                'error_code': get_api_code(value[0]),
                'error_message': value[0],
                'field': key,
            })

    if not new_errors.has_key('error_code'):
        message = 'Validation Failed'
        new_errors['error_code'] = get_api_code(message)
        new_errors['error_message'] = message

    return new_errors


class CommonResponse(object):
    """
    公共响应类, 包含通用的固定API响应

    """
    @staticmethod
    def forbidden():
        """
        没有权限

        """
        return Response(api_error_message('You do not have permission to perform this action.'),
                        status=status.HTTP_403_FORBIDDEN,
                        content_type='application/json')