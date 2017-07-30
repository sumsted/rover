import math

import time

from helpers import settings
from helpers.rovershare import RoverShare

if not settings.sense.test:
    from sense_hat import SenseHat
else:
    from mock.sense_hat import SenseHat


class RoverSense:
    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    BLUE = [0, 0, 255]
    GREEN = [0, 255, 0]
    RED = [255, 0, 0]

    def __init__(self):
        self.sense = SenseHat()
        self.rs = RoverShare()
        self.state = {
            'temperature': 0.0,
            'pressure': 0.0,
            'humidity': 0.0,

            'temperature_base': 0.0,
            'pressure_base': 0.0,
            'humidity_base': 0.0,

            'temperature_delta': 0.0,
            'pressure_delta': 0.0,
            'humidity_delta': 0.0,

            'pitch': 0.0,
            'roll': 0.0,
            'yaw': 0.0,

            'yaw_delta': 0.0,
            'pitch_delta': 0.0,
            'roll_delta': 0.0,

            'pitch_base': 0.0,
            'roll_base': 0.0,
            'yaw_base': 0.0,

            'direction': 0.0,
            'direction_delta': 0.0,
            'direction_base': 0.0,
            'direction_deviation': 0.0
        }
        self.rs.push_status('sense: initialization complete')

    def start(self):
        self.rs.push_status('sense: begin control loop')
        while True:
            # always update sensor data
            self.get_orientation()
            self.get_direction()
            self.get_environment()
            self.rs.update_sense(self.state)

            # process any commands received, should be few
            command = self.rs.pop_sense()
            if command is not None:
                if command['command'] == 'set_heading':
                    self.state['direction_base'] = command['heading']
                    self.rs.push_status('sense: set_heading: %f' % command['heading'])
                elif command['command'] == 'set_correction':
                    self.state['direction_base'] += command['correction']
                    self.rs.push_status('sense: set_correction: %f' % command['correction'])
                elif command['command'] == 'end':
                    self.rs.push_status('sense: end command received')
                    break
                else:
                    self.rs.push_status('sense: unknown command: %s' % command['command'])
            # slow things down
            time.sleep(settings.sense.delay)
        self.rs.push_status('sense: end sense, good bye')

    def set_base(self):
        self.set_direction_base()
        self.set_environment_base()
        self.set_orientation_base()

    def set_heading(self, heading):
        self.set_direction_base(heading)

    def set_environment_base(self):
        self.state['temperature_base'] = self.sense.get_temperature()
        self.state['pressure_base'] = self.sense.get_pressure()
        self.state['humidity_base'] = self.sense.get_humidity()

    def set_direction_base(self, heading=None):
        self.sense.set_imu_config(True, False, False)
        self.state['direction_base'] = heading or self.sense.get_compass()

    def set_orientation_base(self):
        self.sense.set_imu_config(True, True, True)
        orientation_data = self.sense.get_orientation()
        self.state['pitch_base'] = orientation_data['pitch']
        self.state['yaw_base'] = orientation_data['yaw']
        self.state['roll_base'] = orientation_data['roll']
        self.sense.set_imu_config(True, True, True)

    def get_environment(self):
        self.state['temperature'] = self.sense.get_temperature()
        self.state['pressure'] = self.sense.get_pressure()
        self.state['humidity'] = self.sense.get_humidity()
        self.state['temperature_delta'] = self.state['temperature'] - self.state['temperature_base']
        self.state['humidity_delta'] = self.state['humidity'] - self.state['humidity_base']
        self.state['pressure_delta'] = self.state['pressure'] - self.state['pressure_base']

    def get_direction(self):
        self.sense.set_imu_config(True, False, False)
        self.state['direction'] = self.sense.get_compass()
        self.state['direction_delta'] = RoverSense.calculate_delta(self.state['direction'])
        self.state['direction_deviation'] = RoverSense.calculate_deviation(self.state['direction_base'],
                                                                           self.state['direction'])
        self.sense.set_imu_config(True, True, True)

    def get_orientation(self):
        self.sense.set_imu_config(True, True, True)
        orientation_data = self.sense.get_orientation()
        self.state['pitch'] = orientation_data['pitch']
        self.state['yaw'] = orientation_data['yaw']
        self.state['roll'] = orientation_data['roll']
        self.state['pitch_delta'] = RoverSense.calculate_delta(self.state['pitch'])
        self.state['roll_delta'] = RoverSense.calculate_delta(self.state['roll'])
        self.state['yaw_delta'] = RoverSense.calculate_delta(self.state['yaw'])

    @staticmethod
    def calculate_deviation(a1, a2):
        # print(a1, a2)
        d = (a2 - a1)
        d = d * 1.0 if abs(d) < 180.0 else math.copysign(360.0 - abs(d), -d)
        return d

    @staticmethod
    def calculate_delta(val):
        return val if (val >= 0.0 and val <= 180.0) else -(360.0 - val)

    def print_sensor(self):
        for k, v in self.state.items():
            print('%s: %f ' % (k, v), end='')
        print()


if __name__ == "__main__":
    rs = RoverSense()
    rs.start()
