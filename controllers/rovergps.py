import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.rovershare import RoverShare
from helpers.whatthreewords import get_coordinates_from_words, get_words_from_coordinates

if not settings.gps.mock_gps:
    import garmin
else:
    from mock import garmin

import time
from math import pi, sin, cos, atan2, radians, degrees

"""
Uses pygarmin library to pull in current gps state.
Only the even calls to retrieve data have usable data.
Will use what three words to identify destination.
Perhaps add these calls to a helper so that the controller can use it.

"""


# callback from garmin get pvt , not currently used
def gps_pvt_callback(pvt, record_number, total_points_to_get, tp):
    pass


class RoverGps:

    FIX_TYPE = {
        2: '2D',
        3: '3D',
        4: '2D_diff',
        5: '3D_diff'
    }

    def __init__(self):
        self.gps_state = {
            'mock': settings.gps.mock_gps,
            'lat': 0.0,
            'lon': 0.0,
            'three_words': 'a.b.c',
            'altitude_meters': 0.0,
            'altitude_feet': 0.0,
            'position_error_feet': 0.0,
            'altitude_error_feet': 0.0,
            'plane_error_feet': 0.0,
            'destination_lat': 0.0,
            'destination_lon': 0.0,
            'destination_three_words': '',
            'heading': 0.0,
            'fix': 0,
            'last_update': 0.0,
            'delta_seconds': 0.0
        }
        self.rs = RoverShare()
        self.device = garmin.SerialLink(settings.gps.address)
        self.gps = garmin.Garmin(self.device)
        self.gps.pvtOn()
        self.rs.clear_gps_queue()
        self.rs.push_status('gps: initialization complete')

    def start(self):
        self.rs.push_status('gps: begin control loop')
        while True:
            # update gps data when fix is usable
            # seeing some freaky fix values 2500+
            pvt = self.gps.getPvt(gps_pvt_callback)
            if pvt.fix in RoverGps.FIX_TYPE.keys():
                self.get_gps_state(pvt)
                self.rs.update_gps(self.gps_state)

            # process any commands received, should be few
            command = self.rs.pop_gps()
            try:
                if command is not None:
                    if command['command'] == 'set_destination':
                        self.gps_state['destination_lat'] = command['destination_lat'] or 0.0
                        self.gps_state['destination_lon'] = command['destination_lon'] or 0.0
                        self.gps_state['destination_three_words'] = command['destination_three_words'] or ''
                        if self.gps_state['destination_lat'] == 0.0 and self.gps_state['destination_lon'] == 0.0 and \
                                        self.gps_state['destination_three_words'] != '':
                            self.gps_state['destination_lat'], self.gps_state[
                                'destination_lon'] = self.get_coordinates_from_words(
                                self.gps_state['destination_three_words'])
                        else:
                            self.gps_state['destination_three_words'] = self.get_words_from_coordinates(
                                (self.gps_state['destination_lat'], self.gps_state['destination_lon']))
                        self.rs.push_status('gps: destination set')
                    elif command['command'] == 'ping':
                        self.rs.push_status("gps: pong")
                    elif command['command'] == 'end':
                        self.rs.push_status('gps: end command received')
                        break
                    else:
                        self.rs.push_status('gps: unknown command: %s' % command['command'])
            except Exception as e:
                self.rs.push_status('gps: EXCEPTION: command: %s, %s' % (str(command), str(e)))

            # delay to slow things down
            time.sleep(settings.gps.delay)
        self.rs.push_status('gps: end ultra, good bye')

    def get_heading(self, l1, l2):
        rl1 = (radians(l1[0]), radians(l1[1]))
        rl2 = (radians(l2[0]), radians(l2[1]))
        L = -(l1[1] - l2[1])
        RL = radians(L)
        X = cos(rl2[0]) * sin(RL)
        Y = cos(rl1[0]) * sin(rl2[0]) - sin(rl1[0]) * cos(rl2[0]) * cos(RL)
        RB = atan2(X, Y)
        B = (degrees(RB) + 360) % 360
        return B

    def get_gps_state(self, pvt):
        now = time.time()
        self.gps_state['delta_seconds'] = now - self.gps_state['last_update']
        self.gps_state['last_update'] = now
        self.gps_state['fix'] = RoverGps.FIX_TYPE[pvt.fix]
        self.gps_state['lat'] = pvt.rlat * 180 / pi
        self.gps_state['lon'] = pvt.rlon * 180 / pi
        self.gps_state['heading'] = self.get_heading((self.gps_state['lat'], self.gps_state['lon']),
                                                     (self.gps_state['destination_lat'],
                                                      self.gps_state['destination_lon']))
        self.gps_state['altitude_meters'] = pvt.alt + pvt.msl_height
        self.gps_state['altitude_feet'] = self.gps_state['altitude_meters'] * 3.2808398950131
        self.gps_state['position_error_feet'] = pvt.epe * 3.2808398950131
        self.gps_state['altitude_error_feet'] = pvt.epv * 3.2808398950131
        self.gps_state['plane_error_feet'] = pvt.eph * 3.2808398950131

    def get_coordinates_from_words(self, words):
        if settings.gps.what_three_words_on:
            return get_coordinates_from_words(words)
        else:
            return 0.0, 0.0

    def get_words_from_coordinates(self, coordinates):
        if settings.gps.what_three_words_on:
            return get_words_from_coordinates(coordinates)
        else:
            return 'a b c'


if __name__ == '__main__':
    rc = RoverGps()
    rc.start()
