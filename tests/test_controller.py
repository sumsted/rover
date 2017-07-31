import os
import sys

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
            self.fail(msg)
        except AttributeError as e:
            self.fail('no status located')

    def test_forward_go(self):
        self.rs.update_ultrasonic({
            'left': 0.0,
            'lower': 0.0,
            'front': 100.0,
            'right': 0.0,
            'lower_deviation': 0.0
        })

        self.rs.push_command('forward', 30, 20, 50)

        self.assert_status('controller: forward', 'controller forward status not found')

        self.rs.push_command('stop')

        self.assert_status('controller: stop', 'controller stop status not found')

    def test_forward_proximity(self):
        # clear queues
        # clear status
        # set encoders
        # set ultrasonics
        # send command
        # check status
        self.assertEqual(0, 0, "No match")

    def test_lower_proximity(self):
        # clear queues
        # clear status
        # set encoders
        # set ultrasonics
        # send command
        # check status
        self.assertEqual(0, 0, "No match")

    def test_forward_distance_reached(self):
        # clear queues
        # clear status
        # set encoders
        # set ultrasonics
        # send command
        # check status
        self.assertEqual(0, 0, "No match")
