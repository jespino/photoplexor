#!/usr/bin/env python
import pika
import cherrypy
import uuid
import ConfigParser

config = ConfigParser.ConfigParser()
config.readfp(file('config.ini', 'r'))

broker_conf = dict(config.items('broker'))
service_conf = dict(config.items('service'))

connection = pika.BlockingConnection(pika.ConnectionParameters(host=broker_conf['host'], port=int(broker_conf['port'])))
channel = connection.channel()
channel.queue_declare(queue=broker_conf['queue'])

class PhotoPlexor(object):
    @cherrypy.expose
    def index(self, **kwargs):
        if not kwargs:
            return """<html><body>
                        <form method='post' enctype='multipart/form-data'>
                          <label for='photo'>Photo</label>
                          <input id='photo' type='file' name='photo' /><br />
                          <label for='photo'>ID (40 caracters)</label>
                          <input id='id' type='text' name='id' /><br />
                          <input type='submit' value='send' /><br />
                        </form>
                      </body></html>"""
        else:
            photo = kwargs.get('photo', None)
            id = kwargs.get('id', "0000"+str(uuid.uuid4()))
            if not id:
                id = "0000"+str(uuid.uuid4())
            if not photo:
                return "KO: photo parameter is needed"
            if len(id) != 40:
                return "KO: id must be a fixed size 40 caracters string"

            channel.basic_publish(exchange='',
                        routing_key=broker_conf['queue'],
                        body=id+photo.file.read())
            return id
    index.exposed = True

cherrypy.config.update({'server.socket_host': service_conf['bind'], 'server.socket_port': int(service_conf['port']), })
cherrypy.quickstart(PhotoPlexor())
