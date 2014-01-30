#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from . import generate_request_id


class AddRequestIdHeaderMiddleware(object):
    """
    X-Request-ID header is usually added by the web server. We will emulate
    this behaviour here.
    """
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        if "HTTP_X_REQUEST_ID" not in environ:
            environ["HTTP_X_REQUEST_ID"] = generate_request_id()
        return self.app(environ, start_response)
