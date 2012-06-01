Architecture
============

PhotoPlexor have a modular architecture, divided in 5 independant blocks.

Service
-------

The service is a simple REST service (writed on cherrypy) thats received the
images and send it to the worker.

Broker
------

The broker receive and store the images in a queue. Today the only supported
broker is RabbitMQ.

Workers
-------

The workers is a group of process that get images from the broker queue and do
the job (process the images)

Image Processor
---------------

The image procesor is a class that provide the actions (process to apply to the
images) and used by the workers. This class can be replaced by your own
implementation, this give you the oportunity to add actions or modify the
behavior of the current default actions.

Notifier
--------

Library to notify the finish of an image processing. Now only implement a
simple POST method to an URL.
