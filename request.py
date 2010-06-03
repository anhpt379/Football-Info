#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @request - Jun 1, 2010
#  Documentation for this module.
#
#  More details.

from urllib2 import urlopen


request = lambda url: urlopen(url).read()


test_url = "http://127.0.0.1:8888/folder1/test.txt"
print request(test_url)
