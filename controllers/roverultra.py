# todo read ultrasonic sensors 0, 1, 2, 3
'''
    0 1
 2       3

where 0 is low and 1 is high
2 and 3 are high

record a deviation for 0 where the difference indicates a drop or rise above wheel level

'''
from helpers.rovershare import RoverShare


class RoverUltra:
    LEFT = 0
    LOWER = 1
    FRONT = 2
    RIGHT = 3
    LOWER_BASE = 20

    def __init__(self):
        self.state = {
            'left': 0.0,
            'lower': 0.0,
            'front': 0.0,
            'right': 0.0,
            'lower_deviation': 0.0
        }
        self.rs = RoverShare()
        # todo nano address

    def start(self):
        self.rs.push_status('Ultra: begin control loop')
        while True:
            # always update sensor data
            self.state['left'] = self.get_encoder(RoverUltra.LEFT)
            self.state['lower'] = self.get_encoder(RoverUltra.LOWER)
            self.state['front'] = self.get_encoder(RoverUltra.FRONT)
            self.state['right'] = self.get_encoder(RoverUltra.RIGHT)
            self.state['lower_deviation'] = RoverUltra.LOWER_BASE - self.state['lower']
            self.rs.update_sense(self.state)

            # process any commands received, should be few
            command = self.rs.pop_sense()
            if command is not None:
                if command['command'] == 'end':
                    self.rs.push_status('ultra: end command received')
                    break
                else:
                    self.rs.push_status('ultra: unknown command: %s' % command['command'])
        self.rs.push_status('ultra: end ultra, good bye')

    def get_encoder(self, key):
        # todo call serial to nano
        return 0.0
