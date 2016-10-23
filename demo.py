#!/bin/env python
# -*- coding: utf-8 -*-

"""
Demo script. Run:

python.exe demo.py
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import os

import django
from django.conf import settings
from django.conf.urls import url
from django.core.wsgi import get_wsgi_application

basename = os.path.splitext(os.path.basename(__file__))[0]

middleware_settings_name = 'MIDDLEWARE' if django.VERSION[:2] >= (1, 10) else 'MIDDLEWARE_CLASSES'


def rel(*path):
    return os.path.abspath(
        os.path.join(os.path.dirname(__file__), *path)
    ).replace('\\', '/')


if not settings.configured:
    settings.configure(
        DEBUG=True,
        TIMEZONE='UTC',
        INSTALLED_APPS=['request_id'],
        ROOT_URLCONF=basename,
        WSGI_APPLICATION='{}.application'.format(basename),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'DIRS': [rel('tests', 'templates')],
                'OPTIONS': {
                    'context_processors': [
                        'django.template.context_processors.request'
                    ],
                },
            },
        ],
        LOGGING={
            'version': 1,
            'disable_existing_loggers': False,
            'filters': {
                'request_id': {
                    '()': 'request_id.logging.RequestIdFilter'
                }
            },
            'formatters': {
                'console': {
                    'format': '%(asctime)s - %(levelname)-5s [%(name)s] request_id=%(request_id)s %(message)s',
                    'datefmt': '%H:%M:%S'
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'filters': ['request_id'],
                    'class': 'logging.StreamHandler',
                    'formatter': 'console'
                }
            },
            'loggers': {
                '': {
                    'level': 'DEBUG',
                    'handlers': ['console']
                }
            }
        },
        **{
            middleware_settings_name: ['request_id.middleware.RequestIdMiddleware']
        }
    )

# App

from django.views.generic.base import TemplateView
from request_id import get_current_request_id

logger = logging.getLogger('view')


class HelloView(TemplateView):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        logger.info('handling request')
        return super(HelloView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        logger.info('preparing context data')
        return super(HelloView, self).get_context_data(
            current_request_val=get_current_request_id(),
            **kwargs
        )

    def render_to_response(self, context, **response_kwargs):
        logger.info('rendering template')
        return super(HelloView, self).render_to_response(context, **response_kwargs)


urlpatterns = [
    url(r'^$', HelloView.as_view())
]

# WSGI

from request_id.wsgi import AddRequestIdHeaderMiddleware

application = AddRequestIdHeaderMiddleware(get_wsgi_application())

if __name__ == '__main__':
    from django.core.management import call_command

    call_command('runserver', '8000')
