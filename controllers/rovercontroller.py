import os
import sys
import time
sys.path.insert(0, os.path.abspath('..'))
from helpers import settings
from helpers.pid import Pid
from helpers.rovermap import RoverMap
from helpers.rovershare import RoverShare

if not settings.controller.test:
    from helpers import motor
else:
    from mock import motor

"""
RoverController command processor for rover

Other standalone processors exist for 
sense - sense hat including gyro, accel, compass, temp, humid, barom
ultrasonic - left, right, front, lower(front)
encoders - only one at the moment
map - reading sense and ultra and hopefully GPS in future
led - reading sense to display current and expected directions, also status in future

Supporting 
share - all processors use share with redis to communicate through queues(lists) and key value pairs
settings - will read settings for redis and other params from yaml, not yet setup
motor - makes this thing move, talks from controller only directly to nano that supports pwm to controllers

Other
nano1 - using pwm to send to controllers, left right speeds, four wheels
nano2 - encoder on digital interrupt and ultrasonic on analog polling in loop
from pi to nanos is serial usb to usb, with nano providing last sensor check on request for nano2
nano1 takes serial request for each motor, rpi must continue to send requests to maintain movement as
nano1 will halt movement if command not received every half second, safety mechanism
sensehat is connected to rpi bus and communicates over i2c, will post away from pi with cable to prevent 
interference both temp and magnetic, map use joystick to post commands back to controller for diagnostics
"""


class RoverController:

    null_command = {'command': 'null'}

    def __init__(self):
        self.rs = RoverShare()
        self.pid = Pid()
        self.map = RoverMap()
        self.rs.clear_all_queues()
        self.rs.push_status('controller: initialization complete')

    def start(self):
        command = RoverController.null_command
        self.rs.push_status('controller: begin control loop')
        while True:

            new_command = self.rs.pop_command()
            if new_command is not None:
                command = new_command
                self.rs.push_sense('set_base', 0)
                self.rs.push_encoders('set_base', 0)
                motor.stop()

            if command['command'] == 'stop':
                motor.stop()
                self.rs.push_status('controller: stop')
                command = RoverController.null_command

            elif command['command'] == 'forward':
                if new_command is not None:
                    self.rs.push_sense('set_heading', command['heading'])
                    self.rs.push_status('controller: forward, speed: %f, heading: %f, distance: %f' % (
                        command['speed'], command['heading'], command['distance']))

                # pid
                sense = self.rs.get_sense()  # has direction
                direction_change = self.pid.get_correction(sense['direction_deviation'])

                # check distance from obstructions, both straight ahead and drop
                ultrasonic = self.rs.get_ultrasonic()
                if ultrasonic['front'] <= settings.controller.safe_distance or \
                                ultrasonic['lower_deviation'] <= -settings.controller.safe_incline or \
                                ultrasonic['lower_deviation'] >= settings.controller.safe_incline:
                    motor.stop()
                    command['command'] = 'stop'
                    self.rs.push_status(
                        'controller: proximity warning, all stop, front: %f, lower_deviation: %f, lower: %f' % (
                            ultrasonic['front'], ultrasonic['lower_deviation'], ultrasonic['lower']))
                else:
                    # check distance and move
                    encoders = self.rs.get_encoders()
                    if encoders['distance'] >= command['distance']:
                        motor.stop()
                        command['command'] = 'stop'
                        self.rs.push_status('controller: forward distance reached, distance: %f, encoder: %f' % (
                            command['distance'], encoders['distance']))
                    else:
                        if encoders['distance'] % 20 == 0:
                            self.rs.push_status('controller: forward distance travelled: %d' % encoders['distance'])
                        motor.move(command['speed'] + (direction_change / 2),
                                   command['speed'] + (-1 * (direction_change / 2)))

            elif command['command'] == 'rotate':
                # set new direction
                if new_command is not None:
                    angle = command['angle'] if 'angle' in command else None
                    heading = command['heading'] if 'heading' in command else None

                    if angle is None and heading is not None:
                        self.rs.push_sense('set_heading', heading)
                    else:
                        self.rs.push_sense('set_correction', angle)
                    self.rs.push_status('controller: rotate, speed: %f, angle: %f, heading: %f' % (
                        command['speed'], command['angle'] or 500, command['heading'] or 500))

                # get deviation from sense and adjust
                sense = self.rs.get_sense()
                if RoverController.approx(sense['direction_deviation'], sense['direction_base'],
                                          settings.controller.direction_deviation_range):
                    motor.stop()
                    command['command'] = 'stop'
                    self.rs.push_status(
                        'controller: rotation reached, direction: %f, direction_deviation: %f, direction_base: %f' % (
                            sense['direction'], sense['direction_deviation'], sense['direction_base']))
                else:
                    sign = -1 if sense['direction_deviation'] > 0 else 1
                    motor.move(sign * command['speed'] / 2, (sign * -1) * command['speed'] / 2)

            elif command['command'] == 'direct':
                # todo with joystick or other command input
                pass

            elif command['command'] == 'diagnostic':
                # todo diagnostic requerst perhaps from sensehat
                pass

            elif command['command'] == 'end':
                motor.stop()
                self.rs.push_status('controller: end command received, ending all controllers')
                self.rs.push_sense('end', None)
                self.rs.push_encoders('end', None)
                self.rs.push_led('end', None)
                self.rs.push_ultrasonic('end', None)
                self.rs.push_status('controller: sent end command')
                break

            elif command['command'] == 'null':
                pass

            else:
                if new_command is not None:
                    motor.stop()
                    self.rs.push_status('controller: unknown command: %s' % command['command'])

            # slow things down a bit
            time.sleep(settings.controller.delay)

        self.rs.push_status('controller: end rover, good bye')

    @staticmethod
    def approx(x, y, d):
        return True if (x - y) < d else False


if __name__ == '__main__':
    rc = RoverController()
    rc.start()
