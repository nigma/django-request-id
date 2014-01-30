#-*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import uuid

__version__ = "0.1.0"


from .local import Local, release_local

local = Local()


def generate_request_id():
    return uuid.uuid4().__str__()


def get_current_request_id():
    try:
        return local.request_id
    except AttributeError:
        return ""
