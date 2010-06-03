#!/usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311
import sys, os
sys.path.append(os.path.dirname(__file__))

from lib.tornado import wsgi, httpserver, ioloop
from lib.text_processing import xml_format
from lib.database import BetInfo   
from Cheetah.Template import Template
from operator import itemgetter
from time import strftime, localtime
from datetime import date as date_format
from urllib import unquote
from settings import main_menu, info

#reload(sys)
#sys.setdefaultencoding('utf-8')
 
s = os.stat(__file__)
_last_update = s.st_mtime
last_update = strftime("%d-%m-%Y", localtime(_last_update))
 
status = '200 OK'
info['last_update'] = last_update

BET_INFO = BetInfo()    

#====== WSGI Apps ==========
#
def menu(environ, start_response):
  info['menu'] = main_menu
  xml = str(Template(file="templates/menu.xml", searchList=[info]))
  response_headers = [('Content-Type', 'text/xml'),
                      ('Content-Length', str(len(xml)))]
  start_response(status, response_headers)
  return [xml]

def comments(environ, start_response):
  a = open('data/y_kien_chuyen_gia.txt').read().strip()
  comments = [x.strip() for x in a.split('\n\n')]
  info['comments'] = comments
  xml = Template(file="templates/comments.xml", searchList=[info])
  xml = str(xml)
  response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
                      ('Content-Length', str(len(xml)))]
  start_response(status, response_headers)
  return [xml]

def matches(environ, start_response):
  """Lấy danh sách các trận sẽ thi đấu trong Worldcup 2010."""
  matches = []
  for key in BET_INFO.list_keys():
    match = {}
    match['team_1'] = BET_INFO.get(key % 'team_1')
    match['team_2'] = BET_INFO.get(key % 'team_2')
    match['date'] = BET_INFO.get(key % 'date')
    
    t = [int(x) for x in str(match['date']).split('/')]
    if date_format(t[2], t[1], t[0]) > date_format.today():
      match['hour'] = BET_INFO.get(key % 'hour')
      match['href'] = "bet_info|%s - %s (%s)" \
                    % (match['team_1'], match['team_2'], match['date'])
      match['href2'] = "odd_details|%s - %s (%s)" \
                     % (match['team_1'], match['team_2'], match['date'])

      matches.append([match, s])
    else:
      pass
  _data = sorted(matches, key=itemgetter(1))
  
  matches = []
  for row in _data:
    matches.append(row[0])
  info['matches'] = matches
  xml = Template(file="templates/matches.xml", searchList=[info])
  xml = str(xml)
  response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
                      ('Content-Length', str(len(xml)))]
  start_response(status, response_headers)
  return [xml]

def bet_info(environ, start_response):
  match = unquote(environ['PATH_INFO']).split('|')[1]
  key = match + ': %s'
  
  date = BET_INFO.get(key % 'date')
  hour = BET_INFO.get(key % 'hour')
  time = '%s %s' % (date, hour)
  
  team_1 = BET_INFO.get(key % 'team_1')
  team_2 = BET_INFO.get(key % 'team_2')
  
  ah_team_1 = BET_INFO.get(key % "ah_team_1")
  ah_team_2 = BET_INFO.get(key % "ah_team_2")
  ah = BET_INFO.get(key % "ah")
  
  ou_team_1 = BET_INFO.get(key % "ou_team_1")
  ou_team_2 = BET_INFO.get(key % "ou_team_2")
  ou = BET_INFO.get(key % "ou")
    
  ah1st_team_1 = BET_INFO.get(key % "ah1st_team_1")
  ah1st_team_2 = BET_INFO.get(key % "ah1st_team_2")
  ah1st = BET_INFO.get(key % "ah1st")
  
  ou1st_team_1 = BET_INFO.get(key % "ou1st_team_1")
  ou1st_team_2 = BET_INFO.get(key % "ou1st_team_2")
  ou1st = BET_INFO.get(key % "ou1st")
  
  data = """
  <source>%s</source>
  <match>%s</match>
  <time>%s</time>
  <full_time>
    %-15s: +%s  @%s
    %-15s: -%s  @%s
    +%-15s      @%s
    -%-15s      @%s
  </full_time>
  <first_half>
    %-15s: +%s  @%s
    %-15s: -%s  @%s
    +%-15s      @%s
    -%-15s      @%s
  </first_half>
  """ % (BET_INFO.get('source'),
         match, 
         time,
         team_1, ah, ah_team_1,
         team_2, ah, ah_team_2,
         ou, ou_team_1,
         ou, ou_team_2,
         team_1, ah1st, ah1st_team_1,
         team_2, ah1st, ah1st_team_2,
         ou1st, ou1st_team_1,
         ou1st, ou1st_team_2
         )
  data = description % data
  response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
                      ('Content-Length', str(len(data)))]
  start_response(status, response_headers)
  return [data]

def odd_details(environ, start_response):
  match = unquote(environ['PATH_INFO']).split('|')[1]
  key = match + ': %s'
  
  date = BET_INFO.get(key % 'date')
  hour = BET_INFO.get(key % 'hour')
  
  team_1 = BET_INFO.get(key % 'team_1')
  team_2 = BET_INFO.get(key % 'team_2')
  
  ah_team_1 = BET_INFO.get(key % "ah_team_1")
  ah_team_2 = BET_INFO.get(key % "ah_team_2")
  ah = BET_INFO.get(key % "ah")
  
  ou_team_1 = BET_INFO.get(key % "ou_team_1")
  ou_team_2 = BET_INFO.get(key % "ou_team_2")
  ou = BET_INFO.get(key % "ou")
    
  ah1st_team_1 = BET_INFO.get(key % "ah1st_team_1")
  ah1st_team_2 = BET_INFO.get(key % "ah1st_team_2")
  ah1st = BET_INFO.get(key % "ah1st")
  
  ou1st_team_1 = BET_INFO.get(key % "ou1st_team_1")
  ou1st_team_2 = BET_INFO.get(key % "ou1st_team_2")
  ou1st = BET_INFO.get(key % "ou1st")
  
  data = """
  <source>%s</source>
  <date>%s</date>
  <hour>%s</hour>
  <team_1>%s</team_1>
  <team_2>%s</team_2>
  <ah>%s</ah>
  <ah_team_1>%s</ah_team_1>
  <ah_team_2>%s</ah_team_2>
  <ou>%s</ou>
  <ou_team_1>%s</ou_team_1>
  <ou_team_2>%s</ou_team_2>
  <ah1st>%s</ah1st>
  <ah1st_team_1>%s</ah1st_team_1>
  <ah1st_team_2>%s</ah1st_team_2>
  <ou1st>%s</ou1st>
  <ou1st_team_1>%s</ou1st_team_1>
  <ou1st_team_2>%s</ou1st_team_2>
  """ % (BET_INFO.get('source'),
         date,
         hour,
         team_1,
         team_2,
         ah, 
         ah_team_1,
         ah_team_2,
         ou,
         ou_team_1,
         ou_team_2,
         ah1st,
         ah1st_team_1,
         ah1st_team_2,
         ou1st,
         ou1st_team_1,
         ou1st_team_2
         )
  data = description % data
  response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
                      ('Content-Length', str(len(data)))]
  start_response(status, response_headers)
  return [data]

#====== System Controller =============
#
def controller(environ, start_response):
  """ URI Mapper and Controller """
  path = environ['PATH_INFO']
  try:
    # default request
    if path.startswith('/favicon.ico'):
      response_headers = [('Content-Type', 'text/plain; charset="UTF-8"'),
              ('Content-Length', 0)]
      start_response(status, response_headers)
      return ['']
    elif path.startswith('/about'): # something about me :)
      message = """
                <about>
                  <author>
                    AloneRoad
                  </author>
                  
                  <email>
                    AloneRoad@Gmail.com
                  </email>
                  
                  <mobile_phone>
                    +84-167-345-0-799
                  </mobile_phone>
                </about>
                """
      data = description % message
      response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
                ('Content-Length', str(len(message)))]
      start_response(status, response_headers)
      return [data] 
    
    # my app run here
    elif path.startswith('/menu'):
      return menu(environ, start_response)
    
    elif path.startswith('/comments'):
      return comments(environ, start_response)
    
    elif path.startswith('/matches'):
      return matches(environ, start_response)
    
    elif path.startswith('/bet_info'):
      return bet_info(environ, start_response)
    
    elif path.startswith('/odd_details'):
      return odd_details(environ, start_response)
    
    # not found
    else:
      message = """<error>
              <status_code>400</status_code>
              <description>Yêu cầu không hợp lệ</description>
             </error>"""
      data = description % message
      response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
                ('Content-Length', str(len(message)))]
      start_response(status, response_headers)
      return [data]  
  except KeyboardInterrupt: # 500 Internal Server Error
    message = """
    <error>
      <status_code>500</status_code>
      <description>
        Opps! Thực lòng tôi không mong muốn lỗi này xuất hiện đâu :(
      </description>
    </error>"""
    data = description % message
    response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
              ('Content-Length', str(len(message)))]
    start_response(status, response_headers)
    return [data] 

if __name__ == '__main__':
  try:
    port = int(sys.argv[1])
  except:
    print """
    running on 8000...
    """
#    sys.exit()
    port = 8000

  container = wsgi.WSGIContainer(controller)   
  http_server = httpserver.HTTPServer(container) 
  http_server.listen(port)             
  ioloop.IOLoop.instance().start()    