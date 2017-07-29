import json

import redis


class RoverShare:

    host = '192.168.3.6'
    port = 6379
    command_queue_key = 'command_queue'
    sense_key = 'sense'
    sense_queue_key = 'sense_queue'
    encoders_key = 'encoders'
    encoders_queue_key = 'encoders_queue'
    status_list_key = 'status_list'
    ultrasonic_key = 'ultrasonic'

    def __init__(self):
        self.r = redis.Redis(RoverShare.host, RoverShare.port)

    def clear_commands(self):
        return self.r.delete(RoverShare.command_queue_key)

    def push_command(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.command_queue_key, serial_json)

    def pop_command(self):
        serial_json = self.r.rpop(RoverShare.command_queue_key).decode()
        return json.loads(serial_json)

    def clear_sense_queue(self):
        return self.r.delete(RoverShare.sense_queue_key)

    def push_sense(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.sense_queue_key, serial_json)

    def pop_sense(self):
        serial_json = self.r.rpop(RoverShare.sense_queue_key).decode()
        return json.loads(serial_json)

    def clear_encoders_queue(self):
        return self.r.delete(RoverShare.encoders_queue_key)

    def push_encoders(self, command, parameter):
        command = {'command': command, 'parameter': parameter}
        serial_json = json.dumps(command)
        return self.r.lpush(RoverShare.encoders_queue_key, serial_json)

    def pop_encoders(self):
        serial_json = self.r.rpop(RoverShare.encoders_queue_key).decode()
        return json.loads(serial_json)

    def update_sense(self, sense):
        serial_json = json.dumps(sense)
        return self.r.set(RoverShare.sense_key, serial_json)

    def get_sense(self):
        serial_json = self.r.get(RoverShare.sense_key).decode()
        return json.loads(serial_json)

    def get_ultrasonic(self):
        serial_json = self.r.get(RoverShare.ultrasonic_key).decode()
        return json.loads(serial_json)

    def update_encoders(self, encoders):
        serial_json = json.dumps(encoders)
        return self.r.set(RoverShare.encoders_key, serial_json)

    def get_encoders(self):
        serial_json = self.r.get(RoverShare.encoders_key).decode()
        return json.loads(serial_json)

    def clear_status(self):
        return self.r.delete(RoverShare.status_list_key)

    def push_status(self, status):
        return self.r.lpush(RoverShare.status_list_key, status)

    def pull_last_status(self):
        return self.r.lindex(RoverShare.status_list_key, 0).decode()

    def pull_list_n_status(self, num=10):
        return [x.decode() for x in self.r.lrange(RoverShare.status_list_key, 0, num - 1)]


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
    print(rs.update_sensors({'dd':34, 'dx': 40}))
    print(rs.get_sensors())
    print(rs.get_sensors())
    print(rs.update_sensors({'dd':35, 'dx': 41}))
    print(rs.get_sensors())
    print(rs.update_sensors({'dd':-10, 'dx': 42}))
    print(rs.get_sensors())
    print(rs.update_sensors({'dd':-20, 'dx': 43}))
    print(rs.get_sensors())

    print('status')
    print(rs.clear_status())
    for i in range(20):
        print(rs.push_status("status %d"%i))

    rs.pull_last_status()
    for s in rs.pull_list_n_status(10):
        print(s)

    rs.pull_last_status()
    for s in rs.pull_list_n_status(5):
        print(s)
