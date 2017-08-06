

class SerialLink:
    def __init__(self,address):
        pass

class Garmin:
    class pvt:
        rlat = 0.61192381006
        rlon = -1.5649429166
        alt = 84.7099990845
        msl_height = 30.130941391
        epe = 11.608174324
        epv = 9.39999961853
        eph = 13.6219997406
        fix = 3

    def __init__(self, serial_link):
        pass

    def pvtOn(self):
        pass

    def getPvt(self, callback):
        return self.pvt
