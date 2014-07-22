# -*- coding: utf-8 -*-

import datetime
import json
import logging

from django.utils import timezone
from django.http import HttpResponse
from annoying.functions import get_config
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import status
from rest_framework import authentication

from .models import Token
from .serializers import GetAuthTokenSerializer, RefreshAuthTokenSerializer


logger = logging.getLogger(__name__)


class GetObtainAuthToken(ObtainAuthToken):
    serializer_class = GetAuthTokenSerializer
    authentication_classes = ()

    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.object['user'])

            utc_now = timezone.now()
            if not created and token.created < utc_now - datetime.timedelta(seconds=get_config('AUTHTOKEN_EXPIRE_SECOND')):
                logger.debug('token created: %(token_datetime)s, expire datetime: %(expire_datetime)s', {
                    'token_datetime': token.created,
                    'expire_datetime': utc_now - datetime.timedelta(seconds=get_config('AUTHTOKEN_EXPIRE_SECOND'))
                })
                token.delete()
                token = Token.objects.create(user=serializer.object['user'])
                token.save()

            response_data = {'token': token.key, 'refresh_token': token.rkey}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse(json.dumps(serializer.process_errors()), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)


class RefreshObtainAuthToken(ObtainAuthToken):
    serializer_class = RefreshAuthTokenSerializer
    authentication_classes = ()

    model = Token

    def post(self, request):
        serializer = self.serializer_class(data=request.DATA)
        if serializer.is_valid():
            token = serializer.object['token']
            user = token.user

            token.delete()
            token = Token.objects.create(user=user)
            token.save()

            response_data = {'token': token.key, 'refresh_token': token.rkey}
            return HttpResponse(json.dumps(response_data), content_type="application/json")
        else:
            return HttpResponse(json.dumps(serializer.process_errors()), content_type="application/json", status=status.HTTP_400_BAD_REQUEST)