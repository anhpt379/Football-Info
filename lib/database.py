#! /usr/bin/python
#! coding: utf-8
from lib.redis import Redis
from hashlib import md5
from settings import HOST, COMMENT, RESULT, CACHE, BET_INFO

class BetInfo:
    def __init__(self):
        self.db = Redis(host=HOST, db=BET_INFO)
    
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
    
class Comment:
    def __init__(self):
        self.db = Redis(host=HOST, db=COMMENT)
    
    def set(self, key, value):
        key = md5(key).hexdigest()
        return self.db.set(key, value)
    
    def get(self, key):
        key = md5(key).hexdigest()
        return self.db.get(key)
    
    def remove(self, key):
        key = md5(key).hexdigest()
        return self.db.delete(key)
    
class Cache:
    def __init__(self):
        self.db = Redis(host=HOST, db=CACHE)
    
    def set(self, key, value):
        key = md5(key).hexdigest()
        return self.db.set(key, value)
    
    def get(self, key):
        key = md5(key).hexdigest()
        return self.db.get(key)
    
    def flush(self):
        return self.db.flushdb()
    
class Result:
    def __init__(self):
        self.db = Redis(host=HOST, db=RESULT)
    
    def set(self, key, value):
        key = md5(key).hexdigest()
        return self.db.set(key, value)
    
    def get(self, key):
        key = md5(key).hexdigest()
        return self.db.get(key)

    def remove(self, key):
        key = md5(key).hexdigest()
        return self.db.delete(key)