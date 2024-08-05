import sys

sys.path.insert(0, '')
from src.constant import PATH_OUT

from src.resolution.resolve import control

from src.entity.instance.instance import Instance

#INSEREZ LE NOM DE L'INSTANCE ICI
name = "didactic"
budget_calc = 20000
nb_perm = 30

instance = Instance(name)

instance.load_instance()

control(PATH_OUT,instance,budget_calc,nb_perm)

