import json
import os
import sys

sys.path.insert(0, os.path.abspath('..'))
from helpers import settings

if not settings.motors.test:
    import serial
else:
    from mock import serial


class Motor:
    PACKET = "%1s%04d%04d!"

    def __init__(self):
        self.device = serial.Serial(settings.motors.address, 9600, timeout=.5)

    def write_packet(self, packet):
        print('writing to device: %s' % packet)
        num_bytes = self.device.write(packet.encode())
        print('bytes written: %d' % num_bytes)
        return num_bytes

    def read_packet(self):
        return self.device.readline()

    def move(self, l, r):
        if 100 < l < -100:
            return None
        else:
            packet = Motor.PACKET % ('F', l, r)
            self.write_packet(packet)
            result = self.read_packet()
            return json.loads(result.decode())

    def stop(self):
        pass


def left():
    pass


def right():
    pass


def rotate(r):
    pass


if __name__ == '__main__':
    m = Motor()

    for l in range(-100, 101):
        for r in range(-100, 101):
            print(m.move(l, r))
