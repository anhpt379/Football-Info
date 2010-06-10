#!/usr/bin/python

import sys
import time
import glob
import httplib
import urllib

recepients = []

recepients.append("-------------")

world_text_username = "your@email.com"
world_text_password = "your password"


def send_sms(msg):
    global recepients, world_text_username, world_text_password

    print "Asked to send sms: %s" % msg

    for r in recepients:
        params = ""
        params = params + "username=" + world_text_username
        params = params + "&password=" + world_text_password
        params = params + "&" + urllib.urlencode({'message': msg})
        params = params + "&sourceaddr=SMSAlert"
        params = params + "&mobile=" + r
        print params
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        conn = httplib.HTTPConnection("sms.world-text.com:1081")
        conn.request("POST", "/sendsms", params, headers)
        conn.close();

if __name__ == "__main__":
  send_sms("asdf")
