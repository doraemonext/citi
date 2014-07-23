# -*- coding: utf-8 -*-

import datetime
import warnings

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.core import validators

from rest_framework import ISO_8601
from rest_framework.compat import smart_text, timezone, parse_datetime
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


class CustomDateTimeField(fields.DateTimeField):
    default_error_messages = {
        'required': 'Required data',
        'invalid': 'Invalid data',
    }

    def from_native(self, value):
        if value in validators.EMPTY_VALUES:
            return None

        if isinstance(value, datetime.datetime):
            return value
        if isinstance(value, datetime.date):
            value = datetime.datetime(value.year, value.month, value.day)
            if settings.USE_TZ:
                # For backwards compatibility, interpret naive datetimes in
                # local time. This won't work during DST change, but we can't
                # do much about it, so we let the exceptions percolate up the
                # call stack.
                warnings.warn("DateTimeField received a naive datetime (%s)"
                              " while time zone support is active." % value,
                              RuntimeWarning)
                default_timezone = timezone.get_default_timezone()
                value = timezone.make_aware(value, default_timezone)
            return value

        for format in self.input_formats:
            if format.lower() == ISO_8601:
                try:
                    parsed = parse_datetime(value)
                except (ValueError, TypeError):
                    pass
                else:
                    if parsed is not None:
                        return parsed
            else:
                try:
                    parsed = datetime.datetime.strptime(value, format)
                except (ValueError, TypeError):
                    pass
                else:
                    return parsed

        msg = self.error_messages['invalid']
        raise ValidationError(msg)


class CustomTagField(fields.WritableField):
    def from_native(self, value):
        if type(value) is not list:
            raise ValidationError('Invalid data')
        return value

    def to_native(self, value):
        if type(value) is not list:
            return [tag.name for tag in value.all()]
        return value