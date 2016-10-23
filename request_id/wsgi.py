# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from . import generate_request_id
from .defaults import DEFAULT_REQUEST_ID_HEADER_NAME


class AddRequestIdHeaderMiddleware(object):
    """
    X-Request-ID header is usually added by the web server. We will emulate
    this behaviour here.
    """

    HEADER_NAME = DEFAULT_REQUEST_ID_HEADER_NAME

    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        environ.setdefault(self.HEADER_NAME, generate_request_id())
        return self.app(environ, start_response)
