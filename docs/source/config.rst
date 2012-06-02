Configuration
=============

PhotoPlexor is configured all in one uniq file, the config.ini. This ini file is divided in 4 sections and N size definitions.

Sections
--------

global
~~~~~~

Global behavior options:

    - image_processor: The Image Processor class, you only have to modify this parameter if you want use your own processor class.
    - store_original: If you say "no" here the original posted file will by deleted when the processing is finished.
    - on_finish_image_post: Url to notify when finish all the sizes of an image.

service
~~~~~~~

The REST service options:

    - port: TCP port to use
    - bind: IP to bind (0.0.0.0 for public access)

broker
~~~~~~

The broker access options:

    - server: The broker server type, now only supported rabbitmq.
    - host: Host where is the broker
    - port: Por to access to the broker
    - user: Username to acces to the broker
    - password: Password to access to the broker
    - queue: Queue to deposit the images

workers
~~~~~~~

The workers options:

    - forks: Number of workers forks (1 means no fork, only main process)

Sizes definitions
-----------------

You can define diferent sizes or process to the images recieved. All sizes will
be executed and generate diferent files results. To define a size or process,
you have to create a section on the config.ini like [size:the-name-of-my-size].

On this section you can configure this parameters:

    - width: Final width of the image (used on scale, crop and fit actions)
    - height: Final height of the image (used on scale, crop and fit actions)
    - actions: A comma delimited list of actions (crop, scale, fit, watermark, update_master, grayscale, flip, mirror, equalize, invert)
    - fit_align: Horizontal align (center, left, right) (used on fit)
    - fit_valign: Vertical align (middle, top, botton) (used on fit)
    - crop_align: Horizontal align (center, left, right) (used on crop)
    - crop_valign: Vertical align (middle, top, botton) (used on crop)
    - format: Output format file (used on save, executed alwais)
    - filename: A python string for the output filename (used on save)
    - dstdir: A python string for the output destination directory (used on save)
    - watermark_image: Path to the watermark image (used on watermark)
    - watermark_scale: Scale watermark image before apply (used on watermark)
    - watermark_opacity: The opacity of the watermark image (0.0 to 1.0) (used on watermark)
    - on_finish_post: Url to notify when finish this size processing.

Config Example
--------------

::

  [global]
  image_processor=imageprocs.default.DefaultImageProc
  store_original=no
  on_finish_image_post=http://localhost:8081
  
  [service]
  port=8080
  bind=127.0.0.1
  
  [broker]
  server=rabbitmq
  host=127.0.0.1
  port=5672
  user=photoplexor
  password=photoplexor
  queue=photoplexor
  
  [workers]
  forks=4
  
  [size:example1]
  width=1024
  height=768
  actions=fit,watermark
  fit_align=center
  fit_valign=middle
  format=png
  filename=%(id)s-%(width)sx%(height)s.%(format)s
  dstdir=data/%(width)sx%(height)s
  watermark_image=../example_data/watermark.png
  watermark_scale=no
  watermark_opacity=0.5
  
  [size:example2]
  width=800
  height=600
  actions=crop
  crop_align=center
  crop_valign=middle
  format=png
  filename=%(id)s-%(width)sx%(height)s.%(format)s
  dstdir=data/%(width)sx%(height)s
  watermark_image=../example_data/watermark.png
  watermark_scale=yes
  watermark_opacity=0.5
  on_finish_post=http://localhost:8081
