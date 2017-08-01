# todo use to update heading instead of pushing to the sense hat
from helpers.rovershare import RoverShare


class Navigate:

    def __init__(self):
        self.rs = RoverShare()

    def update_direction(self, direction, delta):
        if direction is not None:
            self.rs.update_direction(direction)
        else:
            self.rs.change_direction(delta)
