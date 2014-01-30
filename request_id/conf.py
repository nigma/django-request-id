#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.conf import settings

from appconf import AppConf


class RequestIdAppConf(AppConf):

    #: Default header name as defined in
    #:`heroku request-id <https://devcenter.heroku.com/articles/http-request-id>`_
    HEADER = "HTTP_X_REQUEST_ID"
