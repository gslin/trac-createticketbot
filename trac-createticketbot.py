#!/usr/bin/env python3

import configparser
import os
import xmlrpc.client

class TracCreateTicketBot(object):
    def __init__(self):
        pass

    def start(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/trac-createticketbot/config.ini'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        uri = c['default']['uri']
        s = xmlrpc.client.ServerProxy(uri)

if '__main__' == __name__:
    t = TracCreateTicketBot()
    t.start()
