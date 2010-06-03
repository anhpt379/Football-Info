#! /usr/bin/python
#! coding: utf-8
from os import system

def update():
    system('git pull')

def start_crawler():
    system('python crawler.py &')

def start_server():
    system('python controller.py')

def start_database():
    system('bin/redis/redis-server bin/redis/redis.conf')

def build():
    system('python configure.py')

def start_all():
    start_database()
    start_crawler()
    start_server()

if __name__ == '__main__':
    start_all()
