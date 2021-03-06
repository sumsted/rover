from helpers.rovershare import RoverShare


class RoverMap:

    def __init__(self):
        self.r_map = {}
        self.rs = RoverShare()
        self.rs.clear_map()

    def add_item(self, x, y, val):
        self.rs.add_map(x, y, val)

    def load_map(self):
        self.r_map = self.rs.get_map()

    def get_range(self):
        x_low = 0
        x_high = 0
        y_low = 0
        y_high = 0
        for x in self.r_map:
            if x > x_high:
                x_high = x
            if x < x_low:
                x_low = x
            for y in self.r_map[x]:
                if y > y_high:
                    y_high = y
                if y < y_low:
                    y_low = y
        return x_low, x_high, y_low, y_high

    def print_map(self):
        self.load_map()
        full_range = self.get_range()
        print("    ", end='')
        for x in range(full_range[0], full_range[1] + 1):
            print(" %2d " % x, end='')
        print("")
        for y in range(full_range[3], full_range[2] - 1, -1):
            print(" %2d " % y, end='')
            for x in range(full_range[0], full_range[1] + 1):
                try:
                    print("  %s " % self.r_map[x][y], end='')
                except KeyError:
                    print("    ", end='')
            print("")


'''
 5 4 3 2 1 0 1 2 3 4 5
5              x
4
3
2    x
1
0          x       x
1
2
3          x
4
5  x               x x

'''

if __name__ == '__main__':
    r = RoverMap()
    r.add_item(0, 0, 'x')
    r.add_item(2, 5, 'x')
    r.add_item(-3, 2, 'x')
    r.add_item(4, 0, 'x')
    r.add_item(0, -3, 'x')
    r.add_item(-4, -5, 'x')
    r.add_item(4, -5, 'x')
    r.add_item(5, -5, 'x')
    r.add_item(0, -3, 'z')
    r.print_map()
