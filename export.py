#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @export - Jun 3, 2010
#  Documentation for this module.
#
#  More details.

from os.path import join
from database import Screen
from simplejson import loads, dumps


db = Screen()

_write = lambda filename, data: open(filename, "w").write(data)

def export():
  try:
    data_folder = '/home/Workspace/FootballInfo2010/data/'
    for i in db.get_list():
      filename = join(data_folder, i + '.txt')
      data = dumps(loads(db.get(i)), indent=2)
      _write(filename, data)
    return 'True'
  except KeyboardInterrupt:
    return 'False'

if __name__ == "__main__":
  export()
