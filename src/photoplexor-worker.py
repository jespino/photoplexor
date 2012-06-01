#!/usr/bin/env python
import pika
import cherrypy
import uuid
import os
import ConfigParser
import StringIO
from imageprocs import ImageProc

config = ConfigParser.RawConfigParser()
config.readfp(file('config.ini', 'r'))

class ImageSize(object):
    def __init__(self, size):
        self.name = size
        self.config = dict(config.items("size:%s" % size))
        self.width = self.config.pop('width')
        self.height = self.config.pop('height')

broker_conf = dict(config.items('broker'))
sizes = [ ImageSize(section[5:]) for section in config.sections() if section.startswith('size:') ]

connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                        host=broker_conf['host'],
                        port=int(broker_conf['port'])
                )
             )
channel = connection.channel()
channel.queue_declare(queue=broker_conf['queue'])

def callback(ch, method, properties, body):
    id = body[0:40]
    print " [x] Received %r" % (id,)
    im_proc = ImageProc(id, body[40:], config)

    for size in sizes:
        print " [x] Generating size %s" % (size.name)

        # Try to run the policy as ImageProc method
        im = getattr(im_proc, size.config['policy'])(size)
        im_proc.save(size, im, id)

channel.basic_consume(callback, queue=broker_conf['queue'], no_ack=True)

print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
