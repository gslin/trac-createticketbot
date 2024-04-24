#!/usr/bin/env python3

import configparser
import datetime
import json
import os
import sys
import time
import xmlrpc.client

class TracGetTicketBot(object):
    def __init__(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/trac-createticketbot/config.ini'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        uri = c['default']['uri']
        self.s = xmlrpc.client.ServerProxy(uri)

    def start(self):
        id = sys.argv[1]
        ticket = self.s.ticket.get(id)

        # Use customized conv() to workaround the following error:
        # Object of type DateTime is not JSON serializable
        print(json.dumps(ticket, default=conv, sort_keys=True, indent=2))

def conv(o):
    return o.__str__()

if '__main__' == __name__:
    t = TracGetTicketBot()
    t.start()
