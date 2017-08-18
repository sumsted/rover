import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from helpers.rovershare import RoverShare

rs = RoverShare()

rs.push_sense('end')
rs.push_ultrasonic('end',None)
rs.push_command('end')
rs.push_led('end', None)
rs.push_encoders('end', None)
rs.push_gps('end')