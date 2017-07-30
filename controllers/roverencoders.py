import time

from helpers import settings
from helpers.rovershare import RoverShare


class RoverEncoders:

    def __init__(self):
        self.ticks = 0
        self.distance = 0
        self.base_ticks = 0
        self.base_distance = 0
        self.state = {
            'ticks': 0,
            'ticks_base': 0,
            'ticks_delta': 0,
            'distance': 0
        }
        self.rs = RoverShare()

    def start(self):
        self.rs.push_status('encoders: begin control loop')
        while True:
            # always update sensor data
            self.state['ticks'] = self.get_encoder()
            self.state['ticks_delta'] = self.state['ticks'] - self.state['ticks_base']
            self.state['distance'] = (self.state[
                                          'ticks_delta'] / settings.encoders.rotation_ticks) * settings.encoders.circumference_cm
            self.rs.update_encoders(self.state)

            # process any commands received, should be few
            command = self.rs.pop_sense()
            if command is not None:
                if command['command'] == 'set_base':
                    self.set_base()
                elif command['command'] == 'end':
                    self.rs.push_status('encoders: end command received')
                    break
                else:
                    self.rs.push_status('encoders: unknown command: %s' % command['command'])
            # slow it down
            time.sleep(settings.encoders.delay)
        self.rs.push_status('encoders: end encoders, good bye')

    def set_base(self):
        self.state['ticks_base'] = self.state['ticks']

    def get_encoder(self):
        # todo send command to serial post response
        a = settings.encoders.address
        return 0
