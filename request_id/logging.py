# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

import logging

from . import get_current_request_id


class RequestIdFilter(logging.Filter):
    def filter(self, record):
        record.request_id = get_current_request_id()
        return True
