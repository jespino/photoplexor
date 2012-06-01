#!/usr/bin/env python
import pika
import cherrypy
import uuid
import os
import ConfigParser
import StringIO
from imageprocs import ImageProc
import datetime

from notifier import notify
import os

config = ConfigParser.RawConfigParser()
config.readfp(file('config.ini', 'r'))

class ImageSize(object):
    def __init__(self, size):
        self.name = size
        self.config = dict(config.items("size:%s" % size))
        self.width = int(self.config.pop('width'))
        self.height = int(self.config.pop('height'))

broker_conf = dict(config.items('broker'))
sizes = [ ImageSize(section[5:]) for section in config.sections() if section.startswith('size:') ]

for x in range(int(config.get('workers','forks'))-1):
    if os.fork() != 0:
        break

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
    notify_url = config.get('global', 'on_finish_image_post')
    try:
        im_proc = ImageProc(id, body[40:], config)
    except IOError:
        print "TODO: IOError: Meter esto en un log"
        notify(notify_url, id, False)
        return False

    for size in sizes:
        print " [x] Generating size %s" % (size.name)

        im = None
        for policy in size.config['policy'].split(','):
            # Try to run the policy as ImageProc method
            im = getattr(im_proc, policy)(size, image=im)

        image_notify_url = size.config.get('on_finish_post', None)
        if image_notify_url:
            notify(image_notify_url, id, True, size.name)

        im_proc.save(size, im, id)
    print " [x] Finished %s at %s" % (id, datetime.datetime.now())

    if notify_url:
        notify(notify_url, id, True)


channel.basic_consume(callback, queue=broker_conf['queue'], no_ack=True)

print ' [*] Waiting for messages. To exit press CTRL+C'
channel.start_consuming()
