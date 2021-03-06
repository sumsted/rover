import os
import sys

import time

sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.rovershare import RoverShare

from unittest import TestCase


class TestController(TestCase):

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
            'rear': 0.0,
            'lower_deviation': 0.0
        })
        self.rs.update_encoders({
            'right': 0,
            'right_base': 0,
            'right_delta': 0,
            'left': 0,
            'left_base': 0,
            'left_delta': 0,
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

    def test_ping(self):
        self.rs.push_command('ping')
        self.delay()
        self.assert_status('controller: pong', 'controller not responding to ping')

    def test_forward(self):
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': 0.0
        })

        self.rs.push_command('forward', 30, 20, 50)
        self.delay()
        self.assert_status('controller: forward', 'controller forward status not found')

        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    def test_forward_proximity(self):
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': 0.0
        })

        self.rs.push_command('forward', 30, 20, 50)
        self.delay()
        self.assert_status('controller: forward', 'controller forward status not found')

        self.rs.clear_status()
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 10.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': 0.0
        })
        self.delay()
        self.assert_n_status('controller: proximity warning', 'controller proximity warning status not found')

        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    # todo use test case once reverse setup in controller
    def _rear_proximity(self):
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': 0.0
        })

        self.rs.push_command('forward', -30, 20, 50)
        self.delay()
        self.assert_status('controller: forward', 'controller forward status not found')

        self.rs.clear_status()
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 10.0,
            'rear': 0.0,
            'lower_deviation': 0.0
        })
        self.delay()
        self.assert_n_status('controller: proximity warning', 'controller proximity warning status not found')

        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    def test_lower_positive_proximity(self):
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': 0.0
        })

        self.rs.push_command('forward', 30, 20, 50)
        self.delay()
        self.assert_status('controller: forward', 'controller forward status not found')

        self.rs.clear_status()
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': 51.0
        })
        self.delay()
        self.assert_n_status('controller: proximity warning', 'controller lower positive proximity warning status not found')

        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    def test_lower_negative_proximity(self):
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': 0.0
        })

        self.rs.push_command('forward', 30, 20, 50)
        self.delay()
        self.assert_status('controller: forward', 'controller forward status not found')

        self.rs.clear_status()
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': -51.0
        })
        self.delay()
        self.assert_n_status('controller: proximity warning', 'controller lower negative proximity warning status not found')

        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    def test_forward_distance_reached(self):
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'rear': 0.0,
            'lower_deviation': 0.0
        })

        self.rs.push_command('forward', 30, 20, 50)
        self.delay()
        self.assert_status('controller: forward', 'controller forward status not found')

        self.rs.clear_status()
        self.rs.update_encoders({
            'ticks': 0,
            'ticks_base': 0,
            'ticks_delta': 0,
            'distance': 51
        })
        self.delay()
        self.assert_n_status('controller: forward distance reached', 'controller expected distance reached not found')

        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    def test_rotate_angle(self):
        self.rs.push_command('rotate', speed=50, angle=90)
        self.delay()
        self.assert_n_status('controller: rotate', 'controller rotate status not found')

        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    def test_rotate_heading(self):
        self.rs.push_command('rotate', speed=50, heading=90)
        self.delay()
        self.assert_n_status('controller: rotate', 'controller rotate status not found')

        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    def test_stop(self):
        self.rs.push_command('stop')
        self.delay()
        self.assert_status('controller: stop', 'controller stop status not found')

    def test_unknown_command(self):
        self.rs.push_command('set_your_face', None)
        self.delay()
        self.assert_status('controller: unknown command', 'encoder unknown command status not found')
