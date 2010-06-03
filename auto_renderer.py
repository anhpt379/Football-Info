#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @auto_renderer - Jun 3, 2010
#  Documentation for this module.
#
#  More details.
from database import BetInfo
from datetime import date as date_format
from spitfire.compiler.util import load_template
from operator import itemgetter


BET_INFO = BetInfo()


def chi_tiet_ty_le_ca_cuoc(href):
  match = href
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
  data = {'date': date,
          'time': hour,
          'team_1': team_1,
          'team_2': team_2,
          'ah': ah,
          'ah_team_1': ah_team_1,
          'ah_team_2': ah_team_2,
          'ou': ou,
          'ou_team_1': ou_team_1,
          'ou_team_2': ou_team_2,
          'ah1st': ah1st,
          'ah1st_team_1': ah1st_team_1,
          'ah1st_team_2': ah1st_team_2,
          'ou1st': ou1st,
          'ou1st_team_1': ou1st_team_1,
          'ou1st_team_2': ou1st_team_2}
  template_file = open("/home/Workspace/FootballInfo2010/templates/worldcup_chi_tiet_ty_le_ca_cuoc.json")
  template_file = template_file.read()
  template = load_template(template_file, 'spitfire_tmpl_o4')
  data = template(search_list=[data]).main()
  return data

def worldcup_danh_sach_tran_dau():
  matches = []
  for key in BET_INFO.list_keys():
    match = {}
    match['team1'] = BET_INFO.get(key % 'team_1')
    match['team2'] = BET_INFO.get(key % 'team_2')
    match['date'] = BET_INFO.get(key % 'date')

    t = [int(x) for x in str(match['date']).split('/')]
    if date_format(t[2], t[1], t[0]) > date_format.today():
      match['time'] = BET_INFO.get(key % 'hour')
      s = match['date'] + match['time']
      matches.append([match, s])
    else:
      pass
  _data = sorted(matches, key=itemgetter(1))

  data = {}
  data['matches'] = []
  for row in _data:
    data['matches'].append(row[0])

  template_file = open("/home/Workspace/FootballInfo2010/templates/worlcup_danh_sach_tran_dau.json")
  template_file = template_file.read()
  template = load_template(template_file, 'spitfire_tmpl_o4')
  data = template(search_list=[data]).main()
  return data

if __name__ == "__main__":
#  worldcup_danh_sach_tran_dau()
  print chi_tiet_ty_le_ca_cuoc("Nigeria (N) - Greece (17/06/2010)")
