class controller:
    test = False
    delay = .5
    safe_distance = 10
    safe_incline = 50
    direction_deviation_range = 2.0


class encoders:
    test = False
    delay = .5
    circumference_cm = 20
    rotation_ticks = 5
    address = '/dev/serial1'


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
    address = '/dev/serial1'


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
    host = '192.168.3.6'
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


class client:
    host = '0.0.0.0'
    port = '8088'
