#! /usr/bin/python
#! coding: utf-8
# pylint: disable-msg=W0311
# pylint: disable-msg=E1101

## Secret key:
# '2ce67e8fce3cf88e7afa25f08b0332f8'
#


from lib.server import route, TornadoServer, run, request, response, redirect
from database import Screen, Log
from simplejson import dumps
from jinja2 import Environment, PackageLoader
from ast import literal_eval as eval

import sys
# Use UTF-8 for output
reload(sys)
sys.setdefaultencoding('utf-8')     # IGNORE:E1101


db = Screen()
log = Log()

env = Environment(loader=PackageLoader('views', 'templates'))


@route("/authen")
def set_cookies():
  secret_key = request.params['secret_key']
  if secret_key == '2ce67e8fce3cf88e7afa25f08b0332f8':
      response.COOKIES['secret_key'] = request.GET['secret_key']
  redirect("/manager")

@route("/add")
def add_screen():
  secret_key = request.COOKIES.get('secret_key')
  if secret_key != '2ce67e8fce3cf88e7afa25f08b0332f8':
    return "Authentication Failure!"


  data = request.params
  screen_id = data['screen_id']
  form_title = data["form_title"]

  type = request.params['type']
  if type == "list":
    template = env.get_template('list.json')
    data["items"] = []
    n = 1
    for i in range(1, 220):
      try:
        item = {}
        item['name'] = data["item%d_name" % i]
        try:
          item['href'] = data["item%d_url" % i]
        except KeyError:
          item['href'] = ""

        if item['name'] != "":

          item['id'] = "item%d" % n
          n += 1
          data["items"].append(item)
      except KeyError:
        continue
  elif type == "info":
    template = env.get_template('info.json')
  elif type == "richtext":
    data['richtext'] = data['richtext'].replace("\r\n", " ")
    data['richtext'] = data['richtext'].replace("\"", "\\\"")
    template = env.get_template('richtext.json')
  elif type == "html":
    template = env.get_template('html.json')


  content = template.render(data)
#  content = dumps(eval(content), indent=2)
  db.add_screen(screen_id, form_title, content)
  print content

  template = env.get_template('manager.html')
  data["screens_list"] = db.get_suggest()
  return template.render(data)


@route('/edit')
def edit():
  secret_key = request.COOKIES.get('secret_key')
  if secret_key != '2ce67e8fce3cf88e7afa25f08b0332f8':
    return "Authentication Failure!"

  data = db.get(request.params['screen_id'])
  data = eval(data)
  data["screen_id"] = request.params['screen_id']
  data["form_title"] = db.get_cache(request.params['screen_id'])["form_title"]

  try:
    data["right_button"]["form_title"] = db.get_cache(data["right_button"]["url"])["form_title"]
    data["left_button"]["form_title"] = db.get_cache(data["left_button"]["url"])["form_title"]
  except:
    pass

  if 'items' in data.keys():
    for i in data['items']:
      try:
        form_title = db.get_cache(i["href"])["form_title"]
        if form_title:
          i['form_title'] = form_title
      except:
        continue
  template = env.get_template('edit.html')
  data["screens_list"] = db.get_suggest()
  print data
  return template.render(data)


@route("/manager")
def manager():
  secret_key = request.COOKIES.get('secret_key')
  if secret_key != '2ce67e8fce3cf88e7afa25f08b0332f8':
    return "Authentication Failure!"
  data = {}
  data["screens_list"] = db.get_suggest()
  template = env.get_template('manager.html')
  data["screens_list"] = db.get_suggest()
  return template.render(data)

@route("/remove")
def remove():
  secret_key = request.COOKIES.get('secret_key')
  if secret_key != '2ce67e8fce3cf88e7afa25f08b0332f8':
    return "Authentication Failure!"
  db.remove(request.params['screen_id'])
  data = {}
  data["screens_list"] = db.get_suggest()
  template = env.get_template('manager.html')
  data["screens_list"] = db.get_suggest()
  return template.render(data)

@route("/favicon.ico")
def favicon():
  return ''

@route('/list')
def list():
  try:
    return db.get_list()
  except:
    return 'None'


@route('/:screen_id')
def open(screen_id):
  response.header['Content-Type'] = 'application/json'
  log.insert(request.address)
  data = db.get(screen_id)
  content = dumps(eval(data), indent=2, ensure_ascii=False)
  return content


def stats():
  pass


if __name__ == "__main__":
  import sys
  try:
    port = int(sys.argv[1])
  except:
    port = 8888
  run(server=TornadoServer, port=port)
