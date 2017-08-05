import os
import time
import sys

sys.path.insert(0, os.path.abspath('..'))

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

    ULTRASONIC_GUIDE = {
        'left': [[3, 2], [4, 2]],
        'lower': [[1, 3], [1, 4]],
        'front': [[2, 3], [2, 4]],
        'right': [[3, 5], [4, 5]],
        'rear': [[5, 3], [5, 4]],
    }

    HEART_BEAT = [
        [0, 0, 100, .1],
        [0, 0, 200, .1],
        [0, 0, 255, .1],
        [0, 0, 200, .1],
        [0, 0, 100, .1],
        [0, 0, 200, .1],
        [0, 0, 255, .1],
        [0, 0, 200, .1],
        [0, 0, 100, .1],
    ]

    HEART_BEAT_GUIDE = [
        [3, 3], [3, 4], [4, 3], [4, 4]
    ]

    def __init__(self):
        self.sense = SenseHat()
        self.rs = RoverShare()
        self.led_matrix = [[RoverLed.BLACK for x in range(8)] for y in range(8)]
        self.sense.set_rotation(90)
        self.rs.push_status('led: initialization complete')
        self.beat_index = 0

    def start(self):
        self.rs.push_status('led: begin control loop')
        while True:
            sense = self.rs.get_sense()

            # process any commands received, should be few
            command = self.rs.pop_led()
            try:
                if command is not None:
                    if command['command'] == 'diagnostic':
                        self.rs.push_status('led: diagnostics')
                    elif command['command'] == 'end':
                        self.rs.push_status('led: end command received')
                        break
                    else:
                        self.rs.push_status('led: unknown command: %s' % command['command'])
                else:
                    self.reset_matrix()
                    self.mark_ultrasonic()
                    self.mark_base_direction(sense)
                    self.draw_matrix()
                    self.heart_beat()
            except Exception as e:
                self.rs.push_status('led: EXCEPTION: command: %s, %s' % (str(command), str(e)))
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

    def heart_beat(self):
        self.beat_index = self.beat_index + 1 % 4
        for beat in RoverLed.HEART_BEAT:
            for coordinates in RoverLed.HEART_BEAT_GUIDE:
                self.sense.set_pixel(coordinates[0], coordinates[1], beat[0], beat[1], beat[2])
            time.sleep(beat[3])

    def mark_ultrasonic(self):
        colors = {'left': RoverLed.GREEN, 'lower': RoverLed.GREEN, 'front': RoverLed.GREEN, 'right': RoverLed.GREEN,
                  'rear': RoverLed.GREEN}
        ultrasonic = self.rs.get_ultrasonic()
        for pos in ['left', 'front', 'right', 'rear']:
            if ultrasonic[pos] <= settings.controller.safe_distance:
                colors[pos] = RoverLed.RED
            elif ultrasonic[pos] <= settings.ultra.max:
                colors[pos] = RoverLed.BLUE
        if ultrasonic['lower_deviation'] <= -settings.controller.safe_incline or \
                        ultrasonic['lower_deviation'] >= settings.controller.safe_incline:
            colors['lower'] = RoverLed.RED
        for k in RoverLed.ULTRASONIC_GUIDE:
            for coordinates in RoverLed.ULTRASONIC_GUIDE[k]:
                self.led_matrix[coordinates[0]][coordinates[1]] = colors[k]

    def mark_base_direction(self, sense):
        map_dev = 10
        if sense['direction_deviation'] < 0:
            self.led_matrix[0][3] = RoverLed.RED
            self.led_matrix[0][4] = RoverLed.RED
        else:
            self.led_matrix[0][3] = RoverLed.GREEN
            self.led_matrix[0][4] = RoverLed.GREEN

        for k in RoverLed.DEVIATION_GUIDE:
            if sense['direction_deviation'] > (k - map_dev) and sense['direction_deviation'] < (k + map_dev):
                for coordinates in RoverLed.DEVIATION_GUIDE[k]:
                    self.led_matrix[coordinates[0]][coordinates[1]] = RoverLed.WHITE
                break

    def test_matrix(self):
        self.sense.set_rotation(90)
        self.led_matrix[0][4] = RoverLed.WHITE
        self.led_matrix[0][5] = RoverLed.BLUE
        self.draw_matrix()


if __name__ == '__main__':
    rc = RoverLed()
    rc.start()
