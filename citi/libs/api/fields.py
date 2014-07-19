# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core import validators

from rest_framework.compat import smart_text
from rest_framework import relations, fields


class CustomPrimaryKeyRelatedField(relations.PrimaryKeyRelatedField):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
        'does_not_exist': 'Invalid data',
        'incorrect_type': 'Invalid data',
    }

    def from_native(self, data):
        if self.queryset is None:
            raise Exception('Writable related fields must include a `queryset` argument')

        try:
            return self.queryset.get(pk=data)
        except ObjectDoesNotExist:
            msg = self.error_messages['does_not_exist']
            raise ValidationError(msg)
        except (TypeError, ValueError):
            received = type(data).__name__
            msg = self.error_messages['incorrect_type']
            raise ValidationError(msg)


class CustomCharField(fields.CharField):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }


class CustomIntegerField(fields.IntegerField):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    def __init__(self, *args, **kwargs):
        super(CustomIntegerField, self).__init__(*args, **kwargs)

    def from_native(self, value):
        try:
            value = int(str(value))
        except (ValueError, TypeError):
            raise ValidationError(self.error_messages['invalid'])
        return value


class CustomFloatField(fields.FloatField):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    def from_native(self, value):
        if value in validators.EMPTY_VALUES:
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            msg = self.error_messages['invalid']
            raise ValidationError(msg)


class CustomChoiceField(fields.ChoiceField):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
        'invalid_choice': 'Invalid data',
    }

    def validate(self, value):
        super(CustomChoiceField, self).validate(value)
        if value and not self.valid_value(value):
            raise ValidationError(self.error_messages['invalid_choice'])


class CustomImageField(fields.ImageField):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
        'missing': 'Invalid data',
        'empty': 'Invalid data',
        'max_length': 'Invalid data',
        'contradiction': 'Invalid data',
        'invalid_image': 'Invalid data',
    }