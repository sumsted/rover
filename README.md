# Rover

Code to support a four wheel rover. The rover has the following features:

1. Controlled primarily by raspberry pi(s)
2. Main sensor readings coming from sensehat
3. Ultrasonic and encoder readings coming from nano 
4. Powered by four gear driven motors
5. Using vex 885 controllers
6. PWM for motor controllers sent through a second nano
7. Several modes available, 1)rover mode (rotation, forward, map, avoidance), 2)direct control, 3)autonomous map
8. Starting with mode 1.
9. Only single encoder now used for distance
10. PID driven by direction from sensehat
11. Will add pictures later. Dim approx, 12 in x 18 x 6, with 6 inch diameter wheels, 20 lbs.
12. Motor stall torque around 400 oz inch at 100rpm max, need about 150 oz inch

### Code
Controllers
- controller - main controller, processing commands and directing motors
- sense - sense hat including gyro, accel, compass, temp, humid, barom
- ultrasonic - left, right, front, lower(front)
- encoders - only one at the moment
- map - reading sense and ultra and hopefully GPS in future
- led - reading sense to display current and expected directions, also status in future

Supporting 
- share - all processors use share with redis to communicate through queues(lists) and key value pairs
- settings - will read settings for redis and other params from yaml, not yet setup
- motor - makes this thing move, talks from controller only directly to nano that supports pwm to controllers

Other
- nano1 - using pwm to send to controllers, left right speeds, four wheels
- nano2 - encoder on digital interrupt and ultrasonic on analog polling in loop
- from pi to nanos is serial usb to usb, with nano providing last sensor check on request for nano2
- nano1 takes serial request for each motor, rpi must continue to send requests to maintain movement as
- nano1 will halt movement if command not received every half second, safety mechanism
- sensehat is connected to rpi bus and communicates over i2c, will post away from pi with cable to prevent 
- interference both temp and magnetic, map use joystick to post commands back to controller for diagnostics