# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from uuid import uuid4

from .local import Local, release_local  # NOQA

__version__ = '1.0.0'

default_app_config = 'request_id.apps.RequestIdConfig'

local = Local()


def generate_request_id():
    return str(uuid4())


def get_current_request_id():
    try:
        return local.request_id
    except AttributeError:
        return ''


__all__ = ['get_current_request_id']
