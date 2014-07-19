# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from rest_framework import serializers


logger = logging.getLogger(__name__)


class CustomSerializer(serializers.Serializer):
    @staticmethod
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

    def process_errors(self):
        """
        对 API 错误信息进行处理后输出, 主要为整理格式

        """

        errors = self.errors
        new_errors = {
            'errors': [],
        }

        for key, value in errors.items():
            if key == 'non_field_errors':
                new_errors['error_code'] = self.get_api_code(value[0])
                new_errors['error_message'] = value[0]
            else:
                new_errors['errors'].append({
                    'error_code': self.get_api_code(value[0]),
                    'error_message': value[0],
                    'field': key,
                })

        if not new_errors.has_key('error_code'):
            message = 'Validation Failed'
            new_errors['error_code'] = self.get_api_code(message)
            new_errors['error_message'] = message

        return new_errors
