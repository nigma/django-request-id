# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function, unicode_literals

from django.template import Library

from .. import get_current_request_id

register = Library()


@register.simple_tag(takes_context=True, name='request_id')
def get_request_id(context):
    if 'request' in context:
        request = context['request']
        if hasattr(request, 'request_id'):
            return request.request_id
    return get_current_request_id()
