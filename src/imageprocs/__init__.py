import ConfigParser
from os.path import realpath, dirname, join
from importlib import import_module

__all__ = ('ImageProc',)

config_path = join(dirname(dirname(realpath(__file__))), 'config.ini')

config = ConfigParser.ConfigParser()
config.readfp(file(config_path, 'r'))
img_proc = config.get('global','image_processor')

module_name = ".".join(img_proc.split(".")[0:-1])
class_name = img_proc.split(".")[-1]
ImageProc = getattr(import_module(module_name), class_name)
