#!/usr/bin/env python3

import configparser
import datetime
import getopt
import os
import sys
import time
import xmlrpc.client

class TracCreateTicketBot(object):
    def __init__(self):
        home = os.environ['HOME']
        f_conf = '{}/.config/trac-createticketbot/config.ini'.format(home)

        c = configparser.ConfigParser()
        c.read(f_conf)

        uri = c['default']['uri']
        self.s = xmlrpc.client.ServerProxy(uri)

    def start(self):
        opts, args = getopt.getopt(
            sys.argv[1:],
            '',
            ['component=', 'description=', 'due_date=', 'owner=', 'parents=', 'priority=', 'timeoffset', 'title=']
        )

        a = {}
        title = ''
        description = ''
        timeoffset = 0

        for opt, arg in opts:
            if '--component' == opt:
                a['component'] = arg
            elif '--description' == opt:
                description = arg
            elif '--due_date' == opt:
                now = int(time.time())
                now_todaystart = now - now % 86400
                due_date = now_todaystart + 86400 * int(arg)
                a['due_date'] = datetime.datetime.fromtimestamp(due_date, datetime.timezone.utc)
            elif '--owner' == opt:
                a['owner'] = arg
            elif '--parents' == opt:
                a['parents'] = arg
            elif '--priority' == opt:
                a['priority'] = arg
            elif '--timeoffset' == opt:
                timeoffset = 86400 * int(arg)
            elif '--title' == opt:
                title = arg

        title = time.strftime(title, time.localtime(time.time() + timeoffset))

        id = self.s.ticket.create(title, description, a)
        print('* ticket_id = {}'.format(id))

if '__main__' == __name__:
    t = TracCreateTicketBot()
    t.start()
