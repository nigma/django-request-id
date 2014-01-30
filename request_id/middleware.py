#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from . import generate_request_id, local, release_local
from .conf import settings


def get_request_id(request):
    if hasattr(request, "request_id"):
        return request.request_id
    elif settings.REQUEST_ID_HEADER:
        return request.META.get("HTTP_X_REQUEST_ID", "")
    else:
        return generate_request_id()


class RequestIdMiddleware(object):

    def process_request(self, request):
        request_id = get_request_id(request)
        request.request_id = request_id
        local.request_id = request_id

    def process_response(self, request, response):
        release_local(local)
        return response
