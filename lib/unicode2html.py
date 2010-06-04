#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @lib.unicode2html - Jun 4, 2010
#  Documentation for this module.
#
#  More details.

def htmlencoder(s):
  new_string = ''
  for char in s:
    new_string = new_string + "&#%d;" % ord(char)
  return new_string

print htmlencoder("Phạm tuấn Anh")

