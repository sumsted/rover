

class RoverEncoders:

    CIRCUMFERENCE_CM = 20
    ROTATION_TICKS = 5

    def __init__(self):
        self.base_encoder = 0
        self.base_distance = 0

    def start(self):
        # todo read and post encoder data
        while True:
            val = self.get_encoder()
            distance = (val / RoverEncoders.ROTATION_TICKS) * RoverEncoders.CIRCUMFERENCE_CM
            # todo post to redis
            # todo read redis command

    def set_base(self):
        self.base_encoder = 0
        self.base_distance = 0

    def get_encoder(self):
        return 0



