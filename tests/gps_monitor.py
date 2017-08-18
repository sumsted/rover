import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.rovershare import RoverShare
import time


if __name__=='__main__':
    rs = RoverShare()
    while True:
        g = rs.get_gps()
        rs.push_gps('ping')
        print(g)
        time.sleep(1)
