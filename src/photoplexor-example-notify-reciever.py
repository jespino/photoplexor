#!/usr/bin/env python
import pika
import cherrypy
import uuid
import ConfigParser

class PhotoPlexorNotifyReceiver(object):
    @cherrypy.expose
    def index(self, **kwargs):
        print kwargs.get('id', None)
        print kwargs.get('size', None)
        print kwargs.get('success', None)
    index.exposed = True

cherrypy.config.update({'server.socket_host': "127.0.0.1", 'server.socket_port': 8081, })
cherrypy.quickstart(PhotoPlexorNotifyReceiver())
