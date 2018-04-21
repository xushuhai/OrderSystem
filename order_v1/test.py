#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/4 16:34
# @Author  : Xsh
# @File    : test.py
# @Software: PyCharm

def wsgi_app(self, environ, start_response):
    """
    The actual WSGI application.
    This is not implemented in `__call__` so that middlewares can be applied:
    app.wsgi_app = MyMiddleware(app.wsgi_app)
    """
    with self.request_context(environ):
        rv = self.preprocess_request()
    if rv is None:
        rv = self.dispatch_request()
    response = self.make_response(rv)
    response = self.process_response(response)
    return response(environ, start_response)


def __call__(self, environ, start_response):
    """Shortcut for :attr:`wsgi_app`"""
    return self.wsgi_app(environ, start_response)
