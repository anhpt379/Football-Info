#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311



from settings import list_template


data = {"cache_status": "yes",
        "auto_refresh": 0,
        "form_title": "Test Form Title",
        "left_button": {"type": "select",
                        "name": "Chọn",
                        "href": "ty_le_truc_tuyen/index.txt"},
        "right_button": {"type": "exit",
                         "name": "Thoát"},
        "items_list": [{"href": "http://localhost", "name": "Menu 1"},
                  {"href": "http://localhost", "name": "Menu 2"}]
        }

from spitfire.compiler import util

template = util.load_template(list_template, 'spitfire_tmpl_o4')

print template(search_list=[data]).main()
