#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @test_cookie - Jun 5, 2010
#  Documentation for this module.
#
#  More details.

from lib.server import request, response, route, run


@route('/set', method='GET')
def set_cookie():
    if 'secret_key' in request.GET:
        response.COOKIES['secret_key'] = request.GET['secret_key']
    return 'OK'

@route('/')
def cookie():
    secret_key = request.COOKIES.get('secret_key')
    response.header['Content-Type'] = 'text/plain'
    return 'Hello, %s' % secret_key

run(port=8000)
