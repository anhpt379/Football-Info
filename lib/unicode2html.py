#! /usr/bin/env python
#! coding: utf-8
# pylint: disable-msg=W0311

## @lib.unicode2html - Jun 4, 2010
#  Documentation for this module.
#
#  More details.

#def htmlencoder(s):
#  new_string = ''
#  for char in s:
#    new_string = new_string + "&#%d;" % ord(char)
#  return new_string
#
#print htmlencoder("p ")


test = """
Xin chào bạn, {{name}}
"""
sometext = test


print template.render(name="Tuấn Anh").encode('utf-8')
