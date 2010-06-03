#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @test_template - Jun 3, 2010
#  Documentation for this module.
#
#  More details.
#from lib.server import route, view, run, request
#
#@route('/add')
#def add():
##  try:
##    screen_id = request.params['screen_id']
##    screen_content = unquote(request.params['content'])
##    screen_content = loads(screen_content) # check json format
##    screen_content = dumps(screen_content, indent=2)
##    db.set(screen_id, screen_content)
##    db.add_to_list(screen_id)
##    return 'True'
##  except:
##    return 'False'
#  data = request.params
#  items_list = []
#  if type == "list":
#    data["items_list"] = []
#    for i in range(1, 20):
#      try:
#        item = {}
#        item['name'] = data["item%d_name" % i]
#        item['href'] = data["item%d_url" % i]
#        if item["name"] is not None:
#          items_list.append(item)
#      except KeyError:
#        break
#  print dict(data, items_list=items_list)
#  return dict(data, items_list=items_list)
#
#run(port=8888)

from jinja2 import Template
from views import test_list
from lib.server import jinja2_view as view

@view("add")
def test():
  data = {
    "type": "list",
    "cache": "yes",
    "left_button_type": "select",
    "left_button_name": "Chon",
    "right_button_type": "exit",
    "right_button_name": "Thoát",
    "form_title": "LiveFootball 2010",
    "items": [{"href": "ty_le_truc_tuyen/index.txt", "name": "Tỷ lệ trực tuyến"},
              {"href": "thong_tin_ben_le/index.txt", "name": "Thông tin bên lề"}],
    "auto_refresh": "0",
  }
  screens_list = {"screens_list": [{"screen_id": "test Id", "form_title": "test title"}]}

#  template = Template(test_list)
#  print template.render(data)
  return dict(screens_list)

print test()
