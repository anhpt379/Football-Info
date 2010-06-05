#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @test - May 31, 2010
#  Documentation for this module.
#
#  More details.
from simplejson import dumps
from urllib import urlencode

#menu = {
#  "type": "list",
#  "cache": "yes",
#  "left_button": {"type": "select", "name": "Chọn"},
#  "right_button": {"type": "exit", "name": "Thoát"},
#  "form_title": "LiveFootball 2010",
#  "items": [{"href": "ty_le_truc_tuyen/index.txt", "name": "ỷ lệ trực tuyến"},
#            {"href": "thong_tin_ben_le/index.txt", "name": "Thông tin bên lề"}],
#  "auto_refresh": "0"
#}
#
from urllib import urlopen, quote
#
#
#url = 'http://127.0.0.1:8888/add?' \
#    + urlencode(menu)
#
#print url
#print urlopen(url).read()

## List Screens
url = 'http://127.0.0.1:8888/list'
print urlopen(url).read()

## Get Screen
url = 'http://localhost:8888/open?screen_id=Menu%20ch%C3%ADnh'
print urlopen(url).read()





