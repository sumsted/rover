

# todo read ultrasonic sensors 0, 1, 2, 3
'''
    0 1
 2       3

where 0 is low and 1 is high
2 and 3 are high

record a deviation for 0 where the difference indicates a drop or rise above wheel level

'''

class RoverUltra:


    def __init__(self):
        self.left = 0.0
        self.lower = 0.0
        self.front = 0.0
        self.right = 0.0
        self.lower_deviation = 0.0
