import os
import sys

import time

sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.rovershare import RoverShare
from unittest import TestCase


class TestLed(TestCase):

    def setUp(self):
        self.rs = RoverShare()
        self.rs.clear_all_queues()
        self.rs.clear_status()
        self.rs.update_sense({
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
        })
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 0.0,
            'right': 0.0,
            'lower_deviation': 0.0
        })
        self.rs.update_encoders({
            'ticks': 0,
            'ticks_base': 0,
            'ticks_delta': 0,
            'distance': 0
        })

    def assert_status(self, check, msg):
        s = self.rs.pull_last_status()
        try:
            s.index(check)
        except ValueError:
            self.fail(msg+', '+s)
        except AttributeError as e:
            self.fail('no status located')

    def assert_n_status(self, check, msg, num=50):
        for s in self.rs.pull_list_n_status(num):
            try:
                if s.index(check):
                    return
            except ValueError:
                pass
        self.fail(msg)

    def delay(self, duration=4):
        time.sleep(duration)

    def test_deviation(self):
        self.rs.update_sense({
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
            'direction_deviation': 45.0
        })
        self.delay()
        self.rs.update_sense({
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
            'direction_deviation': -45.0
        })
        self.delay()

    def test_ultrasonic_good(self):
        self.rs.update_ultrasonic({
            'left': 650.0,
            'lower': 60.0,
            'front': 650.0,
            'right': 650.0,
            'lower_deviation': -10.0
        })
        self.delay()

    def test_ultrasonic_proximity_forward(self):
        self.rs.update_ultrasonic({
            'left': 650.0,
            'lower': 60.0,
            'front': 5.0,
            'right': 650.0,
            'lower_deviation': -10.0
        })
        self.delay()

    def test_ultrasonic_proximity_left_right(self):
        self.rs.update_ultrasonic({
            'left': 5.0,
            'lower': 60.0,
            'front': 650.0,
            'right': 5.0,
            'lower_deviation': -10.0
        })
        self.delay()

    def test_ultrasonic_proximity_lower1(self):
        self.rs.update_ultrasonic({
            'left': 650.0,
            'lower': -120.0,
            'front': 650.0,
            'right': 650.0,
            'lower_deviation': -70.0
        })
        self.delay()

    def test_ultrasonic_proximity_lower2(self):
        self.rs.update_ultrasonic({
            'left': 650.0,
            'lower': 70.0,
            'front': 650.0,
            'right': 650.0,
            'lower_deviation': 70.0
        })
        self.delay()

        def test_ultrasonic_map(self):gi
            self.rs.update_ultrasonic({
                'left': 400.0,
                'lower': -10.0,
                'front': 400.0,
                'right': 400.0,
                'lower_deviation': -10.0
            })
            self.delay()


    def test_unknown_command(self):
        self.rs.push_led('set_your_face', None)
        self.delay()
        self.assert_status('led: unknown command', 'encoder unknown command status not found')
