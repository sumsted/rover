

class Pid:

    kp = 0.0
    ki = 0.0
    kd = 0.0

    def __init__(self):
        self.last_error = 0

    def get_correction(self, error):
        self.last_error = error
        return 0

    def fp(self):
        pass

    def fi(self):
        pass

    def pd(self):
        pass