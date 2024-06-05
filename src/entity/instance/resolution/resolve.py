from ..instance import Instance
from ..instance import Data
from ..instance import Dec
from .sub_data import Sub_data
from .init_solution import init_solution

import numpy as np

def control(data: Sub_data, dec = Dec, time_limit : float = 60.0):
    init = init_solution(data, dec)