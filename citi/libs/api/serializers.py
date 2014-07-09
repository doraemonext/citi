# -*- coding: utf-8 -*-

import logging

from django.conf import settings
from rest_framework import serializers


logger = logging.getLogger(__name__)


class CustomSerializer(serializers.Serializer):
    def process_errors(self):
        errors = self.errors

        for key, value in errors.items():
            message = value
            errors[key] = []
            for msg in message:
                try:
                    errors[key].append({
                        'error_code': settings.API_ERROR_CODE[msg],
                        'error_message': msg,
                    })
                except KeyError:
                    logger.error('API: System error when get the code of message "%(message)s"' % {'message': msg})

                    errors[key].append({
                        'error_code': -1,
                        'error_message': msg,
                    })

        return errors