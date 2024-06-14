from ...aff import Aff
from .struct.sub_data import Sub_data
from .init_solution import init_solution
from .algorithm.GVNS import GVNS

import numpy as np

def control(data: Sub_data, time_limit : float = 60.0):
    s = init_solution(data)
    # aff = Aff()
    GVNS(data, s, 20)
    # temp = s.soluce_propre_to_map(data.locations, data.T-1)
    # aff.save_soluce("propre",temp[0],roads = temp[1])
    # aff.clean_M()
    # temp = s.soluce_sales_to_map(data.locations, data.T-1)
    # aff.save_soluce("sale",temp[0],roads = temp[1])

