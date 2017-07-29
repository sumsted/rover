from helpers.rovershare import RoverShare


class RoverEncoders:

    CIRCUMFERENCE_CM = 20
    ROTATION_TICKS = 5

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
        # todo nano address

    def start(self):
        self.rs.push_status('encoders: begin control loop')
        while True:
            # always update sensor data
            self.state['ticks'] = self.get_encoder()
            self.state['ticks_delta'] = self.state['ticks'] - self.state['ticks_base']
            self.state['distance'] = (self.state['ticks_delta'] / RoverEncoders.ROTATION_TICKS) * RoverEncoders.CIRCUMFERENCE_CM
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
                    self.rs.push_status('encoders: unknown command: %s'%command['command'])
        self.rs.push_status('encoders: end encoders, good bye')

    def set_base(self):
        self.state['ticks_base'] = self.state['ticks']

    def get_encoder(self):
        return 0



