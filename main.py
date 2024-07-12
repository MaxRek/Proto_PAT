import sys

sys.path.insert(0, '')
from src.constant import PATH_OUT

from src.resolution.resolve import control

from src.entity.instance.instance import Instance

#INSEREZ LE NOM DE L'INSTANCE ICI
name = "nope"

instance = Instance(name)

instance.load_instance()

control(PATH_OUT,instance,4,2)

