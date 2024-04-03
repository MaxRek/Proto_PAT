import sys
sys.path.insert(0, '')
from src.scripts.findLatLong import replaceLatLong
from src.scripts.demandFiller import demandFiller
from src.constant import PATH_DATA, PATH_FILE_E

from src.entity.aff import Aff

# truc = Aff([47.37412011769598, -2.234728966487376],10)
# truc.df.load_csv()
# truc.add_point(truc.df)
# truc.M.save("map.html")

demandFiller(PATH_DATA,PATH_FILE_E)
