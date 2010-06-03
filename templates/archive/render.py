#! /usr/bin/python
#! coding: utf-8

from Cheetah.Template import Template

template = """
<?xml version="1.0" encoding="UTF-8"?>
<WorlcupOdds version="$version" last_update="$last_update">
  #for $i in $menu
  <menu href="$i.href">$i.name</menu>
  #end for
</WorlcupOdds>
"""
info = {"version": '1.0', 
        "last_update": "21/5/2010",
        "menu":[{"href": "matches", "name": "Matches"},
                {"href": "results", "name": "Results"}]}

menu ={}
xml = Template(file='templates/menu.xml', searchList=[info, menu])
print xml

from spitfire.compiler import util

template = util.load_template(template, 'spitfire_tmpl_o4')
    
print template(search_list=[info]).main()