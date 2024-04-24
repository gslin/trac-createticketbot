#!/usr/bin/env python3

import configparser
import datetime
import getopt
import json
import os
import sys
import time
import xmlrpc.client

class TracUpdateTicketBot(object):
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
            ['action=', 'component=', 'description=', 'due_date=', 'owner=', 'parents=', 'priority=', 'status=', 'summary=']
        )

        id = args[0]
        comment = args[1]

        attrs = {'action': 'leave'}
        for opt, arg in opts:
            if '--action' == opt:
                attrs['action'] = arg
            elif '--component' == opt:
                attrs['component'] = arg
            elif '--description' == opt:
                description = arg
            elif '--due_date' == opt:
                now = int(time.time())
                now_todaystart = now - now % 86400
                due_date = now_todaystart + int(arg)
                attrs['due_date'] = datetime.datetime.fromtimestamp(due_date, datetime.timezone.utc)
            elif '--owner' == opt:
                attrs['owner'] = arg
            elif '--parents' == opt:
                attrs['parents'] = arg
            elif '--priority' == opt:
                attrs['priority'] = arg
            elif '--status' == opt:
                attrs['status'] = arg
            elif '--summary' == opt:
                summary = arg

        ticket = self.s.ticket.get(id)

        # Use customized conv() to workaround the following error:
        # Object of type DateTime is not JSON serializable
        print(json.dumps(ticket, default=conv, sort_keys=True, indent=2))

        attrs['_ts'] = ticket[3]['_ts']
        self.s.ticket.update(id, comment, attrs, True)

def conv(o):
    return o.__str__()

if '__main__' == __name__:
    t = TracUpdateTicketBot()
    t.start()
