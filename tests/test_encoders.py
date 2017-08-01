import os
import sys

import time

sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.rovershare import RoverShare
from unittest import TestCase


class TestEncoders(TestCase):

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

    def test_base(self):
        self.rs.update_encoders({
            'ticks': 1,
            'ticks_base': 0,
            'ticks_delta': 0,
            'distance': 0
        })
        self.rs.push_encoders('set_base', None)
        self.assert_status('encoders: base set', 'encoder base status not found')
        e = self.rs.get_encoders()
        self.assertEqual(e['ticks'], e['ticks_base'], 'encoder ticks base not set')

    def test_unknown_command(self):
        self.rs.push_encoders('set_your_face', None)
        self.delay()
        self.assert_status('encoders: unknown command', 'encoder unknown command status not found')
