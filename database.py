#! /usr/bin/python
#! coding: utf-8
from lib.redis import Redis
from hashlib import md5
from settings import HOST, LOG, RESULT, SCREEN, BET_INFO, PORT, CACHE
from datetime import date, datetime
from ast import literal_eval


class BetInfo:
  def __init__(self):
    self.db = Redis(host=HOST, db=BET_INFO, port=PORT)

  def set(self, key, value):
    key = md5(key).hexdigest()
    return self.db.set(key, value)

  def get(self, key):
    key = md5(key).hexdigest()
    return self.db.get(key)

  def remove(self, key):
    key = md5(key).hexdigest()
    return self.db.delete(key)

  def add_key(self, keyname):
    return self.db.sadd('keys', keyname)

  def list_keys(self):
    return self.db.smembers('keys')


class Log:
  def __init__(self):
    self.db = Redis(host=HOST, db=LOG, port=PORT)

  def insert(self, address):
    self.db.incr("TotalRequest", 1)
    key = md5(address + str(datetime.now())).hexdigest()
    self.db.lpush(str(date.today()), key)
    self.db.set(key, "%s at %s" % (address, str(datetime.now())))
    return True

  def total_request(self, key):
    return self.db.get("TotalRequest")

  def total_request_today(self):
    return self.db.llen(str(date.today()))

  def total_active_today(self):
    all = self.db.lrange(str(date.today()), 0, self.total_request_today())
    return len(list(set(all)))


class Screen:
  def __init__(self):
    self.db = Redis(host=HOST, db=SCREEN, port=PORT)
    self.cache = Redis(host=HOST, db=CACHE, port=PORT)

  def set(self, key, value):
    key = md5(key).hexdigest()
    return self.db.set(key, value)

  def get(self, key):
    key = md5(key).hexdigest()
    return self.db.get(key)

  def add_screen(self, screen_id, form_title, content):
    key = md5(screen_id).hexdigest()
    self.db.set(key, content)
    self.db.sadd("list", key)
    screen = {"screen_id": screen_id, "form_title": form_title}
    self.cache.set(key, str(screen))
    return True

  def get_suggest(self):
    suggest = []
    for i in self.cache.keys():
      suggest.append(literal_eval(self.cache.get(i)))
    return suggest

  def get_cache(self, screen_id):
    key = md5(screen_id).hexdigest()
    return literal_eval(self.cache.get(key))

  def add_to_list(self, key):
    return self.db.sadd("list", key)

  def get_list(self):
    return list(self.db.smembers("list"))

  def flush(self):
    return self.db.flushdb()

class Result:
  def __init__(self):
    self.db = Redis(host=HOST, db=RESULT, port=PORT)

  def set(self, key, value):
    key = md5(key).hexdigest()
    return self.db.set(key, value)

  def get(self, key):
    key = md5(key).hexdigest()
    return self.db.get(key)

  def remove(self, key):
    key = md5(key).hexdigest()
    return self.db.delete(key)
