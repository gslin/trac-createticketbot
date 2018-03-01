#!/usr/bin/env python3

import configparser
import datetime
import getopt
import os
import sys
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
            ['component=', 'description=', 'due_date=', 'owner=', 'parents=', 'priority=', 'title=']
        )

        a = {}
        title = ''
        description = ''

        for opt, arg in opts:
            if '--component' == opt:
                a['component'] = arg
            elif '--description' == opt:
                description = arg
            elif '--due_date' == opt:
                a['due_date'] = datetime.datetime.utcnow() + datetime.timedelta(seconds=86400 * int(arg))
            elif '--owner' == opt:
                a['owner'] = arg
            elif '--parents' == opt:
                a['parents'] = arg
            elif '--priority' == opt:
                a['priority'] = arg
            elif '--title' == opt:
                title = arg

        id = self.s.ticket.create(title, description, a)
        print('* ticket_id = {}'.format(id))

if '__main__' == __name__:
    t = TracCreateTicketBot()
    t.start()
