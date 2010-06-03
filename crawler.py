#! /usr/bin/python
#! coding: utf-8
# pylint: disable-msg=W0311
from time import strftime, strptime
from urllib import urlopen, urlencode
from simplejson import loads
from lib.text_processing import get_text
from database import BetInfo
from settings import REFRESH_TIME
from os import system

BET_INFO = BetInfo()

def http_post(url, form_data):
  cmd = 'curl -d "%s" %s -o "data/odds_data.txt"' % (form_data, url)
  print cmd
  system(cmd)
  return open('data/odds_data.txt').read()


def get_from_sbobet():
  uri = 'http://www.sbobet.com/web_root/public/odds/frame-data.aspx'
  form_data = {'oddsp': '1,3,1,6,0,1,2,1026',
               'synids':-1, 'reload': 0, 'index': 0, 'frame': 8}

  params = urlencode(form_data)
  data = urlopen(uri, params).read()

  if data is not None:
    vars = get_text('parent\.od_Data\[0\]\.c = ', '\;', data)[0]
    # convert vars to python format
    vars = vars.replace('[,,', ', [None, None, ')
    vars = vars.replace('[,', ', [None, ')
    vars = vars.replace(',\r\n,', ',\n')
    vars = vars.replace('[\r\n', '[')
    data = loads(vars)   # convert string to list
    for i in xrange(len(data)):
      try:
        info = data[i][1][0]
        team_1 = info[1]
        team_2 = info[2]
        time = info[4].split()
        date = time[0].split('/')
        date = '%s/%s/2010' % (date[1], date[0])
        hour = time[1]
        key = '%s - %s (%s)' % (team_1, team_2, date)
        key = key + ': %s'

        BET_INFO.add_key(key)
        BET_INFO.set(key % "team_1", team_1)
        BET_INFO.set(key % "team_2", team_2)
        BET_INFO.set(key % "date", date)
        BET_INFO.set(key % "hour", hour)

        bet_info = data[i][2]

        #==== Chấp ====
        #
        ah = bet_info[1][2]
        ah_team_1 = float(ah[2]) + 1
        ah_team_2 = float(ah[3]) + 1
        ah = ah[4]
        if '-' in ah:
          ah = str(ah).split('-')
          ah = (float(ah[0]) + float(ah[1])) / 2
        BET_INFO.set(key % "ah_team_1", ah_team_1)
        BET_INFO.set(key % "ah_team_2", ah_team_2)
        BET_INFO.set(key % "ah", ah)

        ah1st = bet_info[1][6]
        ah1st_team_1 = float(ah1st[2]) + 1
        ah1st_team_2 = float(ah1st[3]) + 1
        ah1st = ah1st[4]
        if '-' in ah1st:
          ah1st = str(ah1st).split('-')
          ah1st = (float(ah1st[0]) + float(ah1st[1])) / 2
        BET_INFO.set(key % "ah1st_team_1", ah1st_team_1)
        BET_INFO.set(key % "ah1st_team_2", ah1st_team_2)
        BET_INFO.set(key % "ah1st", ah1st)

        #==== Trên dưới ======
        #
        ou = bet_info[1][3]
        ou_team_1 = float(ou[2]) + 1
        ou_team_2 = float(ou[3]) + 1
        ou = ou[4]
        if '-' in ou:
          ou = str(ou).split('-')
          ou = (float(ou[0]) + float(ou[1])) / 2
        BET_INFO.set(key % "ou_team_1", ou_team_1)
        BET_INFO.set(key % "ou_team_2", ou_team_2)
        BET_INFO.set(key % "ou", ou)


        ou1st = bet_info[1][7]
        ou1st_team_1 = float(ou1st[2]) + 1
        ou1st_team_2 = float(ou1st[3]) + 1
        ou1st = ou1st[4]
        if '-' in ou1st:
          ou1st = str(ou1st).split('-')
          ou1st = (float(ou1st[0]) + float(ou1st[1])) / 2
        BET_INFO.set(key % "ou1st_team_1", ou1st_team_1)
        BET_INFO.set(key % "ou1st_team_2", ou1st_team_2)
        BET_INFO.set(key % "ou1st", ou1st)

      except TypeError:
        continue
  return None

def get_from_188bet():
  url = 'http://www.188bet.com/Common/Bet188/Odds/OpGetOdds.aspx'
  form_data = 's11StakeType=AH&s11OddsType=HK&s11ViewType=2&i13MarketType=1&s00SportIDList=111&s00LeagueList=&s00MatchNoList=&d00DateRefresh=&i12PageNo=1&i13EMDate=1000&pm=0'

  data = http_post(url, form_data)
  date = get_text('var dt="', '";', data)[0]
  odds = get_text('var odds = ', ';', data)[0]
  odds = loads(odds)
  print odds
  for key in odds.keys():
      odd = odds[key]

      date = odd['info'][6]
      c = strptime(date + ' 2010', "%d %b %Y")
      date = strftime('%d/%m/%Y', c)
      hour = odd['info'][7]

      team_1 = odd['info'][8]
      team_2 = odd['info'][10]
      if '(OVER)' in team_1 or '(OVER)' in team_2:
        continue

      #======== Info ==========
      #
      key = '%s - %s (%s)' % (team_1, team_2, date)
      key = key + ': %s'
      BET_INFO.add_key(key)
      BET_INFO.set(key % "team_1", team_1)
      BET_INFO.set(key % "team_2", team_2)
      BET_INFO.set(key % "date", date)
      BET_INFO.set(key % "hour", hour)

      #======= Chấp ==========
      #
      try:
        ah_team_1 = float(odd['ah'][3]) + 1
        ah = odd['ah'][1]
        ah_team_2 = float(odd['ah'][5]) + 1
        if '/' in ah:
          ah = str(ah).split('/')
          ah = (float(ah[0]) + float(ah[1])) / 2
        BET_INFO.set(key % "ah_team_1", ah_team_1)
        BET_INFO.set(key % "ah_team_2", ah_team_2)
        BET_INFO.set(key % "ah", ah)
      except ValueError:
        BET_INFO.remove(key % "ah_team_1")
        BET_INFO.remove(key % "ah_team_2")
        BET_INFO.remove(key % "ah")

      try:
        ah1st_team_1 = float(odd['ah1st'][3]) + 1
        ah1st = odd['ah1st'][1]
        ah1st_team_2 = float(odd['ah1st'][5]) + 1
        if '/' in ah1st:
          ah1st = str(ah1st).split('/')
          ah1st = (float(ah1st[0]) + float(ah1st[1])) / 2
        BET_INFO.set(key % "ah1st_team_1", ah1st_team_1)
        BET_INFO.set(key % "ah1st_team_2", ah1st_team_2)
        BET_INFO.set(key % "ah1st", ah1st)
      except ValueError:
        BET_INFO.remove(key % "ah1st_team_1")
        BET_INFO.remove(key % "ah1st_team_2")
        BET_INFO.remove(key % "ah1st")

      #============ Trên dưới =============
      #
      try:
        ou = odd['ou'][1]
        ou_team_1 = float(odd['ou'][3]) + 1
        ou_team_2 = float(odd['ou'][5]) + 1
        if '/' in ou:
          ou = str(ou).split('/')
          ou = (float(ou[0]) + float(ou[1])) / 2
        BET_INFO.set(key % "ou_team_1", ou_team_1)
        BET_INFO.set(key % "ou_team_2", ou_team_2)
        BET_INFO.set(key % "ou", ou)
      except ValueError:
        BET_INFO.remove(key % "ou_team_1")
        BET_INFO.remove(key % "ou_team_2")
        BET_INFO.remove(key % "ou")


      try:
        ou1st = odd['ou1st'][1]
        ou1st_team_1 = float(odd['ou1st'][3]) + 1
        ou1st_team_2 = float(odd['ou1st'][5]) + 1
        if '/' in ou1st:
          ou1st = str(ou1st).split('/')
          ou1st = (float(ou1st[0]) + float(ou1st[1])) / 2
        BET_INFO.set(key % "ou1st_team_1", ou1st_team_1)
        BET_INFO.set(key % "ou1st_team_2", ou1st_team_2)
        BET_INFO.set(key % "ou1st", ou1st)
      except:
        BET_INFO.remove(key % "ou1st_team_1")
        BET_INFO.remove(key % "ou1st_team_2")
        BET_INFO.remove(key % "ou1st")



if __name__ == '__main__':
  from time import sleep
  while True:
    print 'Starting...'
    try:
      get_from_188bet()
      BET_INFO.set('source', '188bet.com')
      print 'Crawler status: Done'
      tmp = REFRESH_TIME
      for i in xrange(REFRESH_TIME):
        tmp = tmp - 1
        print 'Refresh in %s...' % (tmp)
        sleep(1)
        system('clear')
    except:
      print '188bet.com error, recrawl from sbobet.com'
      get_from_sbobet()
      BET_INFO.set('source', 'sbobet.com')
      print 'Crawler status: Done'
      tmp = REFRESH_TIME
      for i in xrange(REFRESH_TIME):
        tmp = tmp - 1
        print 'Refresh in %s...' % (tmp)
        sleep(1)
        system('clear')
