from datetime import datetime
import json
import time
import redis

from helpers import settings


class RoverShare:
    host = settings.share.host
    port = settings.share.port
    command_queue_key = settings.share.command_queue_key

    sense_key = settings.share.sense_key
    sense_queue_key = settings.share.sense_queue_key

    encoders_key = settings.share.encoders_key
    encoders_queue_key = settings.share.encoders_queue_key

    ultrasonic_key = settings.share.ultrasonic_key
    ultrasonic_queue_key = settings.share.ultrasonic_queue_key

    gps_key = settings.share.gps_key
    gps_queue_key = settings.share.gps_queue_key

    led_queue_key = settings.share.led_queue_key

    status_list_key = settings.share.status_list_key

    map_hash_key = settings.share.map_hash_key

    def __init__(self):
        self.r = redis.Redis(RoverShare.host, RoverShare.port)

    def clear_all_queues(self):
        self.clear_commands()
        self.clear_encoders_queue()
        self.clear_led_queue()
        self.clear_sense_queue()
        self.clear_ultra_queue()
        self.clear_gps_queue()

    def push_all_end(self):
        self.push_command('end')
        self.push_encoders('end')
        self.push_led('end')
        self.push_sense('end')
        self.push_ultrasonic('end')

    def delay(self, duration=None):
        time.sleep(duration or settings.share.delay)

    ###############################
    # used by main controller
    def clear_commands(self):
        return self.r.delete(RoverShare.command_queue_key)

    def push_command(self, command, speed=None, heading=None, distance=None, angle=None):
        command = {'command': command, 'speed': speed, 'heading': heading, 'distance': distance, 'angle': angle}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.command_queue_key, serial_json)

    def pop_command(self):
        try:
            serial_json = self.r.rpop(RoverShare.command_queue_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    def pull_list_n_command(self, num=10):
        try:
            return [x.decode() for x in self.r.lrange(RoverShare.command_queue_key, 0, num - 1)]
        except AttributeError:
            return None

    ###############################
    # used by sense hat controller
    def clear_sense_queue(self):
        return self.r.delete(RoverShare.sense_queue_key)

    def push_sense(self, command, heading=None, correction=None):
        command = {'command': command, 'heading': heading, 'correction': correction}
        serial_json = json.dumps(command)
        result = self.r.lpush(RoverShare.sense_queue_key, serial_json)
        self.delay()
        return result

    def pop_sense(self):
        try:
            serial_json = self.r.rpop(RoverShare.sense_queue_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # used by encoders controller
    def clear_encoders_queue(self):
        return self.r.delete(RoverShare.encoders_queue_key)

    def push_encoders(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        result = self.r.lpush(RoverShare.encoders_queue_key, serial_json)
        self.delay()
        return result

    def pop_encoders(self):
        try:
            serial_json = self.r.rpop(RoverShare.encoders_queue_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # used by led controller
    def clear_led_queue(self):
        return self.r.delete(RoverShare.led_queue_key)

    def push_led(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        result = self.r.lpush(RoverShare.led_queue_key, serial_json)
        self.delay()
        return result

    def pop_led(self):
        try:
            serial_json = self.r.rpop(RoverShare.led_queue_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # used by ultra controller
    def clear_ultra_queue(self):
        return self.r.delete(RoverShare.ultrasonic_queue_key)

    def push_ultrasonic(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        result = self.r.lpush(RoverShare.ultrasonic_queue_key, serial_json)
        self.delay()
        return result

    def pop_ultrasonic(self):
        try:
            serial_json = self.r.rpop(RoverShare.ultrasonic_queue_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # used by gps controller
    def clear_gps_queue(self):
        return self.r.delete(RoverShare.gps_queue_key)

    def push_gps(self, command, destination_lat=None, destination_lon=None, destination_three_words=None):
        command = {'command': command, 'destination_lat': destination_lat, 'destination_lon': destination_lon,
                   'destination_three_words': destination_three_words}
        serial_json = json.dumps(command)
        result = self.r.lpush(RoverShare.gps_queue_key, serial_json)
        self.delay()
        return result

    def pop_gps(self):
        try:
            serial_json = self.r.rpop(RoverShare.gps_queue_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # sense hat state
    def update_sense(self, sense):
        serial_json = json.dumps(sense)
        return self.r.set(RoverShare.sense_key, serial_json)

    def get_sense(self):
        try:
            serial_json = self.r.get(RoverShare.sense_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # ultrasonic state
    def update_ultrasonic(self, ultrasonic):
        serial_json = json.dumps(ultrasonic)
        return self.r.set(RoverShare.ultrasonic_key, serial_json)

    def get_ultrasonic(self):
        try:
            serial_json = self.r.get(RoverShare.ultrasonic_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # gps state
    def update_gps(self, gps):
        serial_json = json.dumps(gps)
        return self.r.set(RoverShare.gps_key, serial_json)

    def get_gps(self):
        try:
            serial_json = self.r.get(RoverShare.gps_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # encoder state
    def update_encoders(self, encoders):
        serial_json = json.dumps(encoders)
        return self.r.set(RoverShare.encoders_key, serial_json)

    def get_encoders(self):
        try:
            serial_json = self.r.get(RoverShare.encoders_key).decode()
            return json.loads(serial_json)
        except AttributeError:
            return None

    ###############################
    # status list
    def clear_status(self):
        return self.r.delete(RoverShare.status_list_key)

    # todo make status a strucuture that includes seconds as id
    def push_status(self, status):
        now = datetime.now()
        msg = '%s %s' % (now, status or '** chirp chirp **')
        print(msg)
        return self.r.lpush(RoverShare.status_list_key, msg)

    # todo then add a way to pull since passing in id and limit to 100
    def pull_last_status(self):
        try:
            return self.r.lindex(RoverShare.status_list_key, 0).decode()
        except AttributeError:
            return None

    def pull_list_n_status(self, num=10):
        try:
            return [x.decode() for x in self.r.lrange(RoverShare.status_list_key, 0, num - 1)]
        except AttributeError:
            return None

    ###############################
    # map hash
    def clear_map(self):
        return self.r.delete(RoverShare.map_hash_key)

    def add_map(self, x, y, val):
        key = '%08d_%08d' % (x, y)
        serial_json = json.dumps(val)
        return self.r.hset(RoverShare.map_hash_key, key, serial_json)

    def get_map(self):
        try:
            hm = self.r.hgetall(RoverShare.map_hash_key)
            m = {}
            for k, v in hm.items():
                xy = k.decode()
                x = int(xy[0:8])
                y = int(xy[9:17])
                map_val = v.decode()
                try:
                    m[x][y] = json.loads(map_val)
                except KeyError:
                    m[x] = {}
                    m[x][y] = json.loads(map_val)
            return m
        except AttributeError:
            return None


if __name__ == '__main__':
    # push 3 commands
    rs = RoverShare()
    # print('command')
    # print(rs.clear_commands())
    # print(rs.push_command('forward', 50, 40, 30))
    # print(rs.push_command('stop', 0))
    # print(rs.push_command('rotate', 45, 80, 20))
    #
    # print(rs.pop_command())
    # print(rs.pop_command())
    # print(rs.pop_command())

    print('sensors')
    print(rs.update_sense(
        {
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
        }
    ))
    print(rs.get_sense())

    print('encoders')
    print(rs.update_encoders({
        'ticks': 0,
        'ticks_base': 0,
        'ticks_delta': 0,
        'distance': 0
    }))

    print('ultrasonic')
    print(rs.update_ultrasonic({
        'left': 0.0,
        'lower': 0.0,
        'front': 70.0,
        'right': 0.0,
        'lower_deviation': 0.0
    }))
    # print('status')
    # print(rs.clear_status())
    # for i in range(20):
    #     print(rs.push_status("status %d" % i))
    #
    # rs.pull_last_status()
    # for s in rs.pull_list_n_status(10):
    #     print(s)
    #
    # rs.pull_last_status()
    # for s in rs.pull_list_n_status(5):
    #     print(s)
