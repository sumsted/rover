import json
import os
import sys
sys.path.insert(0, os.path.abspath('..'))

if True:
    import serial
else:
    from mock import serial


def get_usb_device(name, default='/dev/ttyUSB0', device_id=None):
    try:
        results = os.popen('dmesg |grep -i "ttyUSB"| grep -i "now attached"').read().split('\n')
        for line in reversed(results):
            print('line: %s'%line)
            if name in line:
                address = '/dev/'+line.split(' ')[-1]
                if device_id is not None:
                    device = serial.Serial(address, 9600, timeout=.5)
                    device.write('I!')
                    result = device.readLine().decode()
                    print(result)
                    device_info = json.loads(result)
                    if device_info['id'] == device_id:
                        return address
                else:
                    return address
    except Exception as e:
        print(e)
    return default


def get_environ(key):
    try:
        return os.environ[key]
    except KeyError:
        return None


class controller:
    test = False
    delay = .5
    safe_distance = 10
    safe_incline = 8
    base_incline = 20
    direction_deviation_range = 2.0


class encoders:
    test = True
    delay = .5
    circumference_cm = 20
    rotation_ticks = 5
    address = get_usb_device('ch341', device_id='encoder')


class motors:
    test = False
    address = get_usb_device('ch341', device_id='motor')


class map:
    pass


class sense:
    test = False
    delay = .5


class led:
    test = False
    delay = .5


class ultra:
    max = 600
    test = False
    delay = .5
    address = get_usb_device('ch341')
    mock_serial = True


class gps:
    key = get_environ('WHAT_THREE_WORDS_KEY')
    address = get_usb_device('Garmin')
    delay = .5
    mock_gps = False
    what_three_words_on = True


class motor:
    pass


class pid:
    test = False
    kp = 0.0
    ki = 0.0
    kd = 0.0
    calibration = 0.0


class share:
    test = False
    # initial deployment will include only one rpi
    #host = '192.168.3.6'
    host = '0.0.0.0'
    port = 6379
    delay = 1.0
    command_queue_key = 'command_queue'
    sense_key = 'sense'
    sense_queue_key = 'sense_queue'
    encoders_key = 'encoders'
    encoders_queue_key = 'ultrasonic_queue'  # sharing controller as hosted on single nano
    status_list_key = 'status_list'
    ultrasonic_key = 'ultrasonic'
    led_queue_key = 'led_queue'
    ultrasonic_queue_key = 'ultrasonic_queue'
    map_hash_key = 'map_hash'
    gps_queue_key = 'gps_queue'
    gps_key = 'gps'


class client:
    host = '0.0.0.0'
    port = '8088'
