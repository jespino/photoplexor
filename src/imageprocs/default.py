import os
from PIL import Image, ImageOps, ImageEnhance

class DefaultImageProc(object):
    def __init__(self, id, image_data, config):
        self.id = id
        file(os.path.join("data", "%s" % (id)), 'w').write(image_data)
        self.im = Image.open(os.path.join("data", "%s" % (id))).convert('RGBA')
        self.config = config

    def __del__(self):
        if self.config.get('global','store_original') == 'no':
            os.unlink(os.path.join("data", "%s" % (self.id)))

    def crop(self, size, image=None):
        if not image:
            image = self.im

        (width, height) = image.size 
        if width >= size.width:
            if size.config['crop_align'] == 'center':
                left = (width/2)-(size.width/2)
                right = (width/2)+(size.width/2)
            elif size.config['crop_align'] == 'left':
                left = 0
                right = size.width
            elif size.config['crop_align'] == 'right':
                left = width-size.width
                right = width
            else:
                raise Exception('Invalid crop_align')
        else:
            left = 0
            right = width

        if height >= size.height:
            if size.config['crop_valign'] == 'middle':
                top = (height/2)-(size.height/2)
                botton = (height/2)+(size.height/2)
            elif size.config['crop_valign'] == 'top':
                top = 0
                botton = size.height
            elif size.config['crop_valign'] == 'botton':
                top = 0
                botton = size.height
            else:
                raise Exception('Invalid crop_valign')
        else:
            top = 0
            botton = height
        return image.crop((left, top, right, botton))

    def fit(self, size, image=None):
        if not image:
            image = self.im

        align = [0.0, 0.0]

        if size.config['fit_align'] == 'center':
            align[1] = 0.5
        elif size.config['fit_align'] == 'left':
            align[1] = 0.0
        elif size.config['fit_align'] == 'right':
            align[1] = 1.0
        else:
            raise Exception('Invalid fit_align')

        if size.config['fit_valign'] == 'middle':
            align[0] = 0.5
        elif size.config['fit_valign'] == 'top':
            align[0] = 0.0
        elif size.config['fit_valign'] == 'botton':
            align[0] = 1.0
        else:
            raise Exception('Invalid fit_valign')
        return ImageOps.fit(image, (size.width, size.height), Image.ANTIALIAS, 0, align)

    def grayscale(self, size, image=None):
        if not image:
            image = self.im

        return ImageOps.grayscale(image)

    def invert(self, size, image=None):
        if not image:
            image = self.im

        return ImageOps.invert(image)

    def flip(self, size, image=None):
        if not image:
            image = self.im

        return ImageOps.flip(image)

    def mirror(self, size, image=None):
        if not image:
            image = self.im

        return ImageOps.mirror(image)

    def equalize(self, size, image=None):
        if not image:
            image = self.im

        return ImageOps.equalize(image)

    def scale(self, size, image=None):
        if not image:
            image = self.im

        return image.resize((size.width, size.height), Image.ANTIALIAS)

    def watermark(self, size, image=None):
        if not image:
            image = self.im

        orig_watermark = Image.open(size.config['watermark_image']).convert('RGBA')
        if size.config['watermark_scale'] == "yes":
            orig_watermark = orig_watermark.resize(image.size, Image.ANTIALIAS)

        watermark = orig_watermark.copy()

        if size.config['watermark_opacity']:
            alpha = watermark.split()[3]
            alpha = ImageEnhance.Brightness(alpha).enhance(float(size.config['watermark_opacity']))
            watermark.putalpha(alpha)
        return Image.composite(orig_watermark, image, watermark)

    def update_master(self, size, image=None):
        self.im = image

    def save(self, size, im, id):
        params = {}
        params.update(size.config)
        params['id'] = id
        params['width'] = size.width
        params['height'] = size.height
        params['name'] = size.name

        filename = size.config['filename'] % params
        dstdir = size.config['dstdir'] % params
        if not os.path.exists(dstdir):
            os.mkdir(dstdir)
        im.save(os.path.join(dstdir, filename))
