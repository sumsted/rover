# todo read ultrasonic sensors 0, 1, 2, 3
"""
    0 1
 2       3

where 0 is low and 1 is high
2 and 3 are high

record a deviation for 0 where the difference indicates a drop or rise above wheel level

"""
import os
import time
import sys
sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.rovershare import RoverShare


class RoverUltraEncoder:
    LEFT = 0
    LOWER = 1
    FRONT = 2
    RIGHT = 3
    LOWER_BASE = 20

    def __init__(self):
        self.ultra_state = {
            'left': 0.0,
            'lower': 0.0,
            'front': 0.0,
            'right': 0.0,
            'lower_deviation': 0.0
        }
        self.encoder_state = {
            'ticks': 0,
            'ticks_base': 0,
            'ticks_delta': 0,
            'distance': 0
        }
        self.rs = RoverShare()
        self.rs.push_status('ultraencoder: initialization complete')

    def start(self):
        self.rs.push_status('ultraencoder: begin control loop')
        while True:
            # always update sensor data
            # ultrasonic and encoder data read
            self.ultra_state['left'] = self.get_ultra(RoverUltraEncoder.LEFT)
            self.ultra_state['lower'] = self.get_ultra(RoverUltraEncoder.LOWER)
            self.ultra_state['front'] = self.get_ultra(RoverUltraEncoder.FRONT)
            self.ultra_state['right'] = self.get_ultra(RoverUltraEncoder.RIGHT)
            self.ultra_state['lower_deviation'] = RoverUltraEncoder.LOWER_BASE - self.ultra_state['lower']
            self.rs.update_ultrasonic(self.ultra_state)

            self.encoder_state['ticks'] = self.get_encoder()
            self.encoder_state['ticks_delta'] = self.encoder_state['ticks'] - self.encoder_state['ticks_base']
            self.encoder_state['distance'] = (self.encoder_state[
                                          'ticks_delta'] / settings.encoders.rotation_ticks) * settings.encoders.circumference_cm
            self.rs.update_encoders(self.encoder_state)

            # process any commands received, should be few
            command = self.rs.pop_ultrasonic()
            try:
                if command is not None:
                    if command['command'] == 'set_base':
                        self.set_encoder_base()
                        self.rs.push_status('ultraencoder: base set')
                    elif command['command'] == 'end':
                        self.rs.push_status('ultraencoder: end command received')
                        break
                    else:
                        self.rs.push_status('ultraencoder: unknown command: %s' % command['command'])
            except Exception as e:
                self.rs.push_status('ultraencoder: EXCEPTION: command: %s, %s' % (str(command), str(e)))
            # delay to slow things down
            time.sleep(settings.ultra.delay)
        self.rs.push_status('ultraencoder: end ultra, good bye')

    def get_ultra(self, key):
        # todo call serial to nano and also check test
        if not settings.ultra.test:
            a = settings.ultra.address
            result = 1.0
        else:
            # mock
            result = 0.0
        return result

    def set_encoder_base(self):
        self.encoder_state['ticks_base'] = self.encoder_state['ticks']

    def get_encoder(self):
        # todo send command to serial post response
        a = settings.encoders.address
        return 0


if __name__ == '__main__':
    rc = RoverUltraEncoder()
    rc.start()
