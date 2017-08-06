import os
import sys

import time

sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.rovershare import RoverShare
from unittest import TestCase


class TestGps(TestCase):

    def setUp(self):
        self.rs = RoverShare()
        self.rs.clear_all_queues()
        self.rs.clear_status()

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

    def test_destination_coordinates(self):
        self.rs.push_gps('set_destination', destination_lat=35.082241, destination_lon=-89.652481)
        self.delay()
        self.assert_status('gps: destination set', 'gps destination status not found')
        g = self.rs.get_gps()
        print(g)
        self.assertEqual(g['destination_three_words'], 'wonderful.saint.batches', 'destination incorrect')

    def test_destination_words(self):
        self.rs.push_gps('set_destination', destination_three_words='wonderful.saint.batches')
        self.delay()
        self.assert_status('gps: destination set', 'gps destination status not found')
        g = self.rs.get_gps()
        print(g)
        self.assertNotEqual(g['destination_lat'], 0.0, 'destination incorrect')

    def test_unknown_command(self):
        self.rs.push_gps('set_your_face', None)
        self.delay()
        self.assert_status('gps: unknown command', 'gps unknown command status not found')
