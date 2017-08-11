import json
import os
import sys

from mock import serial

sys.path.insert(0, os.path.abspath('..'))
from helpers import settings


class Motor:
    PACKET = "%1s%04d%04d!"

    def __init__(self):
        self.device = serial.Serial(settings.motors.address, 9600, timeout=.5)

    def send_packet(self, packet):
        print('writing to device: %s' % self.START_SESSION_PACKET)
        self.device.write(self.START_SESSION_PACKET)

    def read_packet(self):
        return self.device.readline()

    def move(self, l, r):
        if 100 < l < -100:
            return None
        else:
            packet = Motor.PACKET % ('F', l, r)
            self.send_packet(packet)
            result = self.read_packet()
            return json.loads(result)

    def stop(self):
        pass


def left():
    pass


def right():
    pass


def rotate(r):
    pass



if __name__=='__main__':
    m = Motor()
    print(m.move(50,-50))