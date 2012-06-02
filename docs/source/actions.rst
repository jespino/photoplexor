Actions
=======

PhotoPlexor default Image Processor comes with some actions, here you have the
list:

crop
----

Crop the image to adjust the result to the WIDTHxHEIGHT defined size, using the
parameters crop_align and crop_valign to know where to cut.

scale
-----

Simply scale the image (deforming it if not have the same proportion).

fit
---

Scale and crop the image to get the new defined size with a proportional
result, croping out the what is not necesary. The parameters fit_align and
fit_valing allow you to define where to crop.

watermark
---------

Put a watermark on the image using the watermark_image file with the
watermark_opacity as opacity. You can define that the watermark needs to be
scaled with the watermark_scale.

update_master
-------------

Define that actual versión of the image will be the master image.

grayscale
---------

Convert the image to grayscale.

flip
----

Flip the image vertically.

mirror
------

Flip the image horizontally.

equialize
---------

Equalize the image histogram.

invert
------

Invert the colors of the image.
