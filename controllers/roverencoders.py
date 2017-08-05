import os
import time
import sys
sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.rovershare import RoverShare


class RoverEncoders:
    def __init__(self):
        self.ticks = 0
        self.distance = 0
        self.base_ticks = 0
        self.base_distance = 0
        self.encoder_state = {
            'ticks': 0,
            'ticks_base': 0,
            'ticks_delta': 0,
            'distance': 0
        }
        self.rs = RoverShare()
        self.rs.push_status('encoders: initialization complete')

    def start(self):
        self.rs.push_status('encoders: begin control loop')
        while True:
            # always update sensor data
            self.encoder_state['ticks'] = self.get_encoder()
            self.encoder_state['ticks_delta'] = self.encoder_state['ticks'] - self.encoder_state['ticks_base']
            self.encoder_state['distance'] = (self.encoder_state[
                                          'ticks_delta'] / settings.encoders.rotation_ticks) * settings.encoders.circumference_cm
            self.rs.update_encoders(self.encoder_state)

            # process any commands received, should be few
            command = self.rs.pop_encoders()
            if command is not None:
                if command['command'] == 'set_base':
                    self.set_base()
                    self.rs.push_status('encoders: base set')
                elif command['command'] == 'end':
                    self.rs.push_status('encoders: end command received')
                    break
                else:
                    self.rs.push_status('encoders: unknown command: %s' % command['command'])
            # slow it down
            time.sleep(settings.encoders.delay)
        self.rs.push_status('encoders: end encoders, good bye')

    def set_base(self):
        self.encoder_state['ticks_base'] = self.encoder_state['ticks']

    def get_encoder(self):
        # todo send command to serial post response
        a = settings.encoders.address
        return 0


if __name__ == '__main__':
    rc = RoverEncoders()
    rc.rs.push_status('encoders: end encoders - merged into ultraencoder')
    # rc.start()
