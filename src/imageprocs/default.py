import os
from PIL import Image

class DefaultImageProc(object):
    def __init__(self, id, image_data, config):
        self.id = id
        file(os.path.join("data", "%s" % (id)), 'w').write(image_data)
        self.im = Image.open(os.path.join("data", "%s" % (id)))
        self.config = config

    def __del__(self):
        if self.config.get('global','store_original') == 'no':
            os.unlink(os.path.join("data", "%s" % (self.id)))

    def crop(self, size):
        (width, height) = self.im.size 
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
        result_image = Image.new("RGBA", (int(size.width), int(size.height))
        result_image.paste(self.im, (left, top, right, botton))
        return result_image

    def scale(self, size):
        return self.im.resize(size, Image.ANTIALIAS)

    def crop_and_scale(self, size):
        raise NotImplementedError

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
