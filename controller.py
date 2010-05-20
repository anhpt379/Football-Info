#!/usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311
import sys, os
sys.path.append(os.path.dirname(__file__))

from lib.tornado import wsgi, httpserver, ioloop
from lib.text_processing import xml_format, raw_unicode_string
from lib.database import Cache, Comment, Result, BetInfo   
from time import strftime, localtime
from operator import itemgetter
from datetime import date as date_format
from urllib import unquote
from settings import main_menu, delta

reload(sys)
sys.setdefaultencoding('utf-8')     # IGNORE:E1101
 
s = os.stat(__file__)
_last_update = s.st_mtime
last_update = strftime("%d-%m-%Y", localtime(_last_update))
 
status = '200 OK'
description = '<livefootball last_update="%s">' % last_update
description = description + '\n\t%s\n</livefootball>'
BET_INFO = BetInfo()    

#====== WSGI Apps ==========
#
def menu(environ, start_response):
  data = []
  for i in range(len(main_menu)):
    data.append('<menu ref="%s">%s</menu>' % (xml_format(main_menu[i][0]), 
                                              xml_format(main_menu[i][1])))
  data = '\n\t'.join(data)
  data = description % data
  response_headers = [('Content-Type', 'text/xml'),
            ('Content-Length', str(len(data)))]
  start_response(status, response_headers)
  return [data]

def comments(environ, start_response):
  a = open('y_kien_chuyen_gia.txt').read().strip()
  data = ["<comment>%s</comment>" % x.strip() for x in a.split('\n\n')]
  data = '\n  '.join(data)
  data = description % data
  response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
                      ('Content-Length', str(len(data)))]
  start_response(status, response_headers)
  return [data]

def matches(environ, start_response):
  """Lấy danh sách các trận sẽ thi đấu trong Worldcup 2010."""
  data = []
  for key in BET_INFO.list_keys():
    a = BET_INFO.get(key % 'team_1')
    b = BET_INFO.get(key % 'team_2')
    
    date = BET_INFO.get(key % 'date')
    #TODO: Compare with now() to remove finished matches.
    t = [int(x) for x in str(date).split('/')]
    if date_format(t[2], t[1], t[0]) > date_format.today():
      hour = BET_INFO.get(key % 'hour')
      s = '<match ref="bet_info|%s - %s (%s)" time="%s %s">%s - %s</match>' \
                                          % (a, b, date, date, hour, a, b)
      data.append(['%s %s' % (date, hour), s])
    else:
      pass
  _data = sorted(data, key=itemgetter(0))
  
  data = []
  index = 0
  for row in _data:
    data.append(row[1].replace('<match ref', '<match index="%s" ref' % index))
    index += 1

  data = '\n  '.join(data)
  data = description % data
  response_headers = [('Content-Type', 'text/xml; charset="UTF-8"'),
                      ('Content-Length', str(len(data)))]
  start_response(status, response_headers)
  return [data]

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