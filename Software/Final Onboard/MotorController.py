from adafruit_pca9685 import PCA9685
from adafruit_motor import servo, motor
import busio
import board
import time

class MotorController:
    ServoPos = {
        "servo_t":  90,
        "servo_cam_z" : 90,
        "servo_cam_y" : 20,
        "servo_cannon" : 8,
    }
    ServoMax = {
        "servo_t": 160,
        "servo_cam_z": 160,
        "servo_cam_y": 100,
        "servo_cannon": 35,
    }
    ServoMin = {
        "servo_t": 20,
        "servo_cam_z": 20,
        "servo_cam_y": 20,
        "servo_cannon": 0,
    }

    def __init__(self, cp):
        self.CP = cp
        i2c = busio.I2C(board.SCL, board.SDA)
        self.pca = PCA9685(i2c)
        self.pca.frequency = 50
        self.servo_t = servo.Servo(self.pca.channels[0], min_pulse=700, max_pulse=2400)
        self.servo_cam_z = servo.Servo(self.pca.channels[2], min_pulse=700, max_pulse=2400)
        self.servo_cam_y = servo.Servo(self.pca.channels[3], min_pulse=2400, max_pulse=700)
        self.servo_cannon = servo.Servo(self.pca.channels[7], min_pulse=700, max_pulse=2400)
        self.motor_r = servo.ContinuousServo(self.pca.channels[12],min_pulse=700,max_pulse=2400)
        self.motor_l = servo.ContinuousServo(self.pca.channels[15],min_pulse=700, max_pulse=2400)
        self.executeOrders(Orders(49, 49, 49, 49, 1, 1, 0, 0))

    def executeOrders(self, order):
        
        ljx = order.getOrder("ABS_X")
        new_angle_x = self.ServoPos["servo_t"] - ((ljx-49)/49)*3
        if new_angle_x < self.ServoMax["servo_t"] and new_angle_x > self.ServoMin["servo_t"]:
            self.ServoPos["servo_t"] = new_angle_x
            self.servo_t.angle = self.ServoPos["servo_t"]

        ljy = order.getOrder("ABS_Y")
        new_angle_y = self.ServoPos["servo_cannon"] - ((ljy-49)/49)*2
        if new_angle_y < self.ServoMax["servo_cannon"] and new_angle_y > self.ServoMin["servo_cannon"]:
            self.ServoPos["servo_cannon"] = new_angle_y
            self.servo_cannon.angle = self.ServoPos["servo_cannon"]
            
        if order.getOrder("BTN_THUMBL") == 1:
            self.CP.Record()

        new_angle_cz = self.ServoPos["servo_cam_z"] - (order.getOrder("ABS_HAT0X")-1)*2
        if new_angle_cz < self.ServoMax["servo_cam_z"] and new_angle_cz > self.ServoMin["servo_cam_z"]:
            self.ServoPos["servo_cam_z"] = new_angle_cz
            self.servo_cam_z.angle = self.ServoPos["servo_cam_z"]
            

        new_angle_cy = self.ServoPos["servo_cam_y"] - (order.getOrder("ABS_HAT0Y")-1)*2
        if new_angle_cy < self.ServoMax["servo_cam_y"] and new_angle_cy > self.ServoMin["servo_cam_y"]:
            self.ServoPos["servo_cam_y"] = new_angle_cy
            self.servo_cam_y.angle = self.ServoPos["servo_cam_y"]
            

        rjx = (order.getOrder("ABS_RX") - 49) / 49
        rjy = (order.getOrder("ABS_RY") - 49) / 49
        if rjy > 0:
            throttle_r = rjy * 0.3
            throttle_l = rjy * 0.3
            throttle_l += throttle_l * rjx 
            throttle_r -= throttle_r * rjx 
        elif rjy<0:
            throttle_r = rjy * 0.3
            throttle_l = rjy * 0.3
            throttle_l += throttle_l * rjx 
            throttle_r -= throttle_r * rjx 
        else:
            throttle_r = -rjx * 0.5
            throttle_l = rjx * 0.5
            
        acc = order.getOrder("BTN_THUMBR")
        if 0.4 > rjx > -0.4:
            throttle_r += 0.2 * acc
            throttle_l += 0.2 * acc
        self.motor_l.throttle = throttle_l
        self.motor_r.throttle = throttle_r


class Orders:
    # Right Joystick
    ABS_RY = 0
    ABS_RX = 0
    BTN_THUMBR = 0

    # Left Joystick
    ABS_Y = 0
    ABS_X = 0
    BTN_THUMBL = 0

    # Arrow Buttons
    ABS_HAT0Y = 0
    ABS_HAT0X = 0

    def __init__(self, rx, ry, lx, ly, hatx, haty, btnr, btnl):
        self.ABS_RX = rx
        self.ABS_RY = ry
        self.ABS_X = lx
        self.ABS_Y = ly
        self.BTN_THUMBR = btnr
        self.BTN_THUMBL = btnl
        self.ABS_HAT0X = hatx
        self.ABS_HAT0Y = haty
    
    def setOrder(self,msg):
        code = int(int(msg)%10)
        value = int(int(msg)/10)
        if code == 2:
            self.ABS_RY = value
        elif code == 1:
            self.ABS_RX = value
        elif code == 7:
            self.BTN_THUMBR = value
        elif code == 4:
            self.ABS_Y = value
        elif code == 3:
            self.ABS_X = value
        elif code == 8:
            self.BTN_THUMBL = value
        elif code == 6:
            self.ABS_HAT0Y = value
        elif code == 5:
            self.ABS_HAT0X = value
    
    def getOrder(self, code):
        if code == "ABS_RY":
            return self.ABS_RY
        elif code == "ABS_RX":
            return self.ABS_RX
        elif code == "BTN_THUMBR":
            return self.BTN_THUMBR
        elif code == "ABS_Y":
            return self.ABS_Y
        elif code == "ABS_X":
            return self.ABS_X
        elif code == "BTN_THUMBL":
            return self.BTN_THUMBL
        elif code == "ABS_HAT0Y":
            return self.ABS_HAT0Y
        elif code == "ABS_HAT0X":
            return self.ABS_HAT0X