import pigpio
import time

LEFT_PWM = 13
LEFT_DIR = 22
RIGHT_PWM = 12
RIGHT_DIR = 24
lsign = -1
rsign = 1
lt_time = 1.2
rt_time = 1

class Motor:
    def __init__(self, pwm, dp, pi):
        self.pwm = pwm
        self.dir = dp
        self.pi = pi
    
    # speed is a percentage of full
    def set_speed(self, speed, rev=False):
        if rev:
            self.pi.write(self.dir, 0)
        else:
            self.pi.write(self.dir, 1)
        print(rev, self.pi.read(self.dir))
        self.pi.hardware_PWM(self.pwm, 500, int(abs(speed*1e6)))

class Robot:
    # sign to make left or right side go forward with positive speed
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def forward(self, speed):
        self.left.set_speed(speed)
        self.right.set_speed(speed)
    
    def reverse(self, speed):
        self.left.set_speed(speed, rev=True)
        self.right.set_speed(speed, rev=True)
    
    def turn_left(self, speed):
        self.left.set_speed(speed, rev=True)
        self.right.set_speed(speed)
    
    def turn_right(self, speed):
        self.left.set_speed(speed)
        self.right.set_speed(speed, rev=True)
    
    def stop(self):
        self.left.set_speed(0)
        self.right.set_speed(0)

def exec_command(cmd, robot):
    cmd_arr = cmd.split()
    if cmd_arr[0] == 'go':
        if cmd_arr[1]=='forward' or cmd_arr=='forwards':
            robot.forward(1)
        else:
            robot.reverse(1)

        if len(cmd_arr) > 2:
            time.sleep(float(cmd_arr[2]))
            robot.stop()

    elif cmd_arr[0] == 'turn':
        if cmd_arr[1] == 'left':
            robot.turn_left(1)
            time.sleep(lt_time)
            robot.stop()
        else:
            robot.turn_right(1)
            time.sleep(rt_time)
            robot.stop()
    elif cmd_arr[0] == 'stop':
        robot.stop()

def get_robot(leftdir, rightdir, leftpwm, rightpwm):
    pi = pigpio.pi()
    pi.set_mode(LEFT_DIR, pigpio.OUTPUT)
    pi.set_mode(LEFT_PWM, pigpio.OUTPUT)
    pi.set_mode(RIGHT_DIR, pigpio.OUTPUT)
    pi.set_mode(RIGHT_PWM, pigpio.OUTPUT)
    pi.write(LEFT_DIR, 1)
    pi.write(RIGHT_DIR, 1)
    pi.hardware_PWM(LEFT_PWM, 500, 0)
    pi.hardware_PWM(RIGHT_PWM, 500, 0)

    left_motor = Motor(LEFT_PWM, LEFT_DIR, pi)
    right_motor = Motor(RIGHT_PWM, RIGHT_DIR, pi)
    robot = Robot(left_motor, right_motor)
    return robot

    # with open('cmdsequence.txt') as infile:
    #     for line in infile:
    #         exec_command(line, robot)

