#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @server_controller - May 31, 2010
# Remote Controller for Football Info 2010
#
# - Login via SSH with private_key
# - Use rsync to move local files to server
# 
from lib import ssh
from sys import argv

private_key = "/home/Workspace/FootballInfo2010/id_rsa"
remote = ssh.Connection('203.128.246.60', 'root', private_key)

help = """Sử dụng:
  python server_controller.py update | rollback
"""

def update():
  command = "ls -l"
  remote.execute(command)

def rollback():
  pass

def connect():
  pass

def sync():
  pass

if __name__ == '__main__':
  try:
    command = argv[1]
  except IndexError:
    command = None

  if command == "update":
    remote.execute("update command")

  elif command == "rollback":
    remote.execute("rollback command")

  else:
    remote.execute("ls -l /home")
#    print help

