# -*- coding: utf-8 -*-

import json

from django.http import HttpResponse

from libs.api.utils import process_errors, api_success_message


class AjaxResponseMixin(object):
    """
    为 Django Generic Views 提供 Ajax 响应支持

    """
    def render_to_json_response(self, context, **response_kwargs):
        data = json.dumps(context, ensure_ascii=False)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)

    def form_invalid(self, form):
        response = super(AjaxResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(process_errors(form.errors), status=400)
        else:
            return response

    def form_valid(self, form):
        response = super(AjaxResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            return self.render_to_json_response(api_success_message())
        else:
            return response