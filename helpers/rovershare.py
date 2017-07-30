import json

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

    led_queue_key = settings.share.led_queue_key

    status_list_key = settings.share.status_list_key

    map_hash_key = settings.share.map_hash_key

    def __init__(self):
        self.r = redis.Redis(RoverShare.host, RoverShare.port)

    ###############################
    # used by main controller
    def clear_commands(self):
        return self.r.delete(RoverShare.command_queue_key)

    def push_command(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.command_queue_key, serial_json)

    def pop_command(self):
        serial_json = self.r.rpop(RoverShare.command_queue_key).decode()
        return json.loads(serial_json)

    ###############################
    # used by sense hat controller
    def clear_sense_queue(self):
        return self.r.delete(RoverShare.sense_queue_key)

    def push_sense(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.sense_queue_key, serial_json)

    def pop_sense(self):
        serial_json = self.r.rpop(RoverShare.sense_queue_key).decode()
        return json.loads(serial_json)

    ###############################
    # used by encoders controller
    def clear_encoders_queue(self):
        return self.r.delete(RoverShare.encoders_queue_key)

    def push_encoders(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.encoders_queue_key, serial_json)

    def pop_encoders(self):
        serial_json = self.r.rpop(RoverShare.encoders_queue_key).decode()
        return json.loads(serial_json)

    ###############################
    # used by led controller
    def clear_led_queue(self):
        return self.r.delete(RoverShare.led_queue_key)

    def push_led(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.led_queue_key, serial_json)

    def pop_led(self):
        serial_json = self.r.rpop(RoverShare.led_queue_key).decode()
        return json.loads(serial_json)

    ###############################
    # used by ultra controller
    def clear_ultra_queue(self):
        return self.r.delete(RoverShare.ultrasonic_queue_key)

    def push_ultrasonic(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.ultrasonic_queue_key, serial_json)

    def pop_ultrasonic(self):
        serial_json = self.r.rpop(RoverShare.sense_queue_key).decode()
        return json.loads(serial_json)

    ###############################
    # sense hat state
    def update_sense(self, sense):
        serial_json = json.dumps(sense)
        return self.r.set(RoverShare.sense_key, serial_json)

    def get_sense(self):
        serial_json = self.r.get(RoverShare.sense_key).decode()
        return json.loads(serial_json)

    ###############################
    # ultrasonic state
    def update_ultrasonic(self, ultrasonic):
        serial_json = json.dumps(ultrasonic)
        return self.r.set(RoverShare.ultrasonic_key, serial_json)

    def get_ultrasonic(self):
        serial_json = self.r.get(RoverShare.ultrasonic_key).decode()
        return json.loads(serial_json)

    ###############################
    # encoder state
    def update_encoders(self, encoders):
        serial_json = json.dumps(encoders)
        return self.r.set(RoverShare.encoders_key, serial_json)

    def get_encoders(self):
        serial_json = self.r.get(RoverShare.encoders_key).decode()
        return json.loads(serial_json)

    ###############################
    # status list
    def clear_status(self):
        return self.r.delete(RoverShare.status_list_key)

    def push_status(self, status):
        return self.r.lpush(RoverShare.status_list_key, status)

    def pull_last_status(self):
        return self.r.lindex(RoverShare.status_list_key, 0).decode()

    def pull_list_n_status(self, num=10):
        return [x.decode() for x in self.r.lrange(RoverShare.status_list_key, 0, num - 1)]

    ###############################
    # map hash
    def clear_map(self):
        return self.r.delete(RoverShare.map_hash_key)

    def add_map(self, x, y, val):
        key = '%08d_%08d' % (x, y)
        serial_json = json.dumps(val)
        return self.r.hset(RoverShare.map_hash_key, key, serial_json)

    def get_map(self):
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


if __name__ == '__main__':
    # push 3 commands
    rs = RoverShare()
    print('command')
    print(rs.clear_commands())
    print(rs.push_command('forward', 50))
    print(rs.push_command('stop', 0))
    print(rs.push_command('rotate', 45))
    print(rs.push_command('forward', 20))
    print(rs.push_command('heading', 264))

    print(rs.pop_command())
    print(rs.pop_command())
    print(rs.pop_command())

    print('sensors')
    print(rs.update_sense({'dd': 34, 'dx': 40}))
    print(rs.get_sense())
    print(rs.get_sense())
    print(rs.update_sense({'dd': 35, 'dx': 41}))
    print(rs.get_sense())
    print(rs.update_sense({'dd': -10, 'dx': 42}))
    print(rs.get_sense())
    print(rs.update_sense({'dd': -20, 'dx': 43}))
    print(rs.get_sense())

    print('status')
    print(rs.clear_status())
    for i in range(20):
        print(rs.push_status("status %d" % i))

    rs.pull_last_status()
    for s in rs.pull_list_n_status(10):
        print(s)

    rs.pull_last_status()
    for s in rs.pull_list_n_status(5):
        print(s)
