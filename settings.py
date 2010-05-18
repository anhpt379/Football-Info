#! /usr/bin/python
#! coding: utf-8
refresh_time = 60   # Time to re-run crawler

#======= Main Menu ========
#
main_menu = [('matches',  'Tỷ lệ trận đấu'),
             ('results',  'Kết quả các trận đã thi đấu'),
             ('comments', 'Ý kiến chuyên gia'),
             ('tipster',  'Góc tipster'),
             ('news',     'Tin tức Worldcup')]

#======= Comments ========
#
delta = 2   # display comments of next 2 days


#======= Database config ======
#
HOST = 'localhost'
CACHE = 1   # database id
COMMENT = 2
BET_INFO = 3
RESULT = 5

