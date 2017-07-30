import time

from helpers import settings
from helpers.rovershare import RoverShare

if not settings.led.test:
    from sense_hat import SenseHat
else:
    from mock.sense_hat import SenseHat

class RoverLed:

    BLACK = [0, 0, 0]
    WHITE = [255, 255, 255]
    BLUE = [0, 0, 255]
    GREEN = [0, 255, 0]
    RED = [255, 0, 0]
    DEVIATION_GUIDE = {
        0: [[0, 3], [0, 4]],
        -15: [[0, 5]],
        -30: [[0, 6]],
        -45: [[0, 7]],
        -60: [[1, 7]],
        -75: [[2, 7]],
        -90: [[3, 7], [4, 7]],
        -105: [[5, 7]],
        -120: [[6, 7]],
        -135: [[7, 7]],
        -150: [[7, 6]],
        -165: [[7, 5]],
        15: [[0, 2]],
        30: [[0, 1]],
        45: [[0, 0]],
        60: [[1, 0]],
        75: [[2, 0]],
        90: [[3, 0], [4, 0]],
        105: [[5, 0]],
        120: [[6, 0]],
        135: [[7, 0]],
        150: [[7, 1]],
        165: [[7, 2]],
        180: [[7, 3], [7, 4]]
    }

    def __init__(self):
        self.sense = SenseHat()
        self.rs = RoverShare()
        self.led_matrix = [[RoverLed.BLACK for x in range(8)] for y in range(8)]
        self.sense.set_rotation(90)

    def start(self):
        self.rs.push_status('led: begin control loop')
        while True:
            sense = self.rs.get_sense()

            # process any commands received, should be few
            command = self.rs.pop_led()
            if command is not None:
                if command['command'] == 'diagnostic':
                    self.rs.push_status('led: diagnostics')
                elif command['command'] == 'end':
                    self.rs.push_status('led: end command received')
                    break
                else:
                    self.rs.push_status('led: unknown command: %s'%command['command'])
            else:
                self.mark_base_direction(sense)
            # adding delay
            time.sleep(settings.led.delay)
        self.rs.push_status('led: end led, good bye')

    def reset_matrix(self):
        self.led_matrix = [[RoverLed.BLACK for x in range(8)] for y in range(8)]

    def draw_matrix(self):
        pixels = []
        for row in self.led_matrix:
            pixels += row
        self.sense.set_pixels(pixels)

    def mark_base_direction(self, sensors):
        map_dev = 10
        self.reset_matrix()
        if sensors.direction_deviation < 0:
            self.led_matrix[0][3] = RoverLed.RED
            self.led_matrix[0][4] = RoverLed.RED
        else:
            self.led_matrix[0][3] = RoverLed.GREEN
            self.led_matrix[0][4] = RoverLed.GREEN

        for k in RoverLed.DEVIATION_GUIDE:
            if sensors.direction_deviation > (k - map_dev) and sensors.direction_deviation < (k + map_dev):
                for coordinates in RoverLed.DEVIATION_GUIDE[k]:
                    self.led_matrix[coordinates[0]][coordinates[1]] = RoverLed.WHITE
                break
        self.draw_matrix()

    def test_matrix(self):
        self.sense.set_rotation(90)
        self.led_matrix[0][4] = RoverLed.WHITE
        self.led_matrix[0][5] = RoverLed.BLUE
        self.draw_matrix()