#! /usr/bin/python
#! coding: utf-8
import os
os.chdir('bin/redis')
os.system('make')

print 
print 'Done'
print '=' * 80
print """To start server, type:
                python controller.py <port>"""