# coding: utf-8
from functools import wraps

from django.http import HttpRequest

"""
def token_required(func):
    @wraps(func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        return func(request, *args, **kwargs)

    return wrapper
"""
