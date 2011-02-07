#!/usr/bin/env python

PORT = 9000

import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

from socketio import SocketIOServer

import psyco_gevent; psyco_gevent.make_psycopg_green()
from gevent.monkey import patch_thread; patch_thread()

if __name__ == '__main__':
    print 'Listening on port %s and on port 843 (flash policy server)' % PORT
    SocketIOServer(('', PORT), application, resource="socket.io").serve_forever()
