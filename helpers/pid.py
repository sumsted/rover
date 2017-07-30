import time

from helpers import settings
from helpers.rovershare import RoverShare


class Pid:

    kp = settings.pid.kp
    ki = settings.pid.ki
    kd = settings.pid.kd
    calibration = settings.pid.calibration

    def __init__(self):
        self.error_i = 0.0
        self.last_error_p = 0.0
        self.last_error_d = 0.0
        self.last_time = Pid.get_current_milliseconds()
        self.rs = RoverShare()

    def get_correction(self, error_p):
        current_time = Pid.get_current_milliseconds()
        time_elapsed = current_time - self.last_time

        self.error_i += int(error_p * time_elapsed / 1000)
        error_d = 0 if time_elapsed == 0 else (error_p - self.last_error_p) / time_elapsed

        correction = self.kp * error_p + self.ki * self.error_i + self.kd * error_d + self.calibration

        if settings.pid.test:
            msg = "pid: elapsed: %f, kp: %f, ki: %f, kd: %f, ep: %f, ei: %f, ed: %f, correction: %f" % \
                  (time_elapsed, self.kp, self.ki, self.kd, error_p,
                   self.error_i, error_d, correction)
            self.rs.push_status(msg)

        self.last_error_p = error_p
        self.last_time = current_time

        return correction

    @staticmethod
    def get_current_milliseconds():
        return int(round(time.time() * 1000))
