from Command.SerialTransmitter import SerialTransmitter
import inputs


class OrderGenerator:
    observer = SerialTransmitter
    gamepad = inputs.devices.gamepads[0]

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

    def __init__(self, ST):
        self.observer = ST

    def updateCommands(self, code, value):
        if code == "ABS_RY":
            self.ABS_RY = value
        elif code == "ABS_RX":
            self.ABS_RX = value
        elif code == "BTN_THUMBR":
            self.BTN_THUMBR = value
        elif code == "ABS_Y":
            self.ABS_Y = value
        elif code == "ABS_X":
            self.ABS_X = value
        elif code == "BTN_THUMBL":
            self.BTN_THUMBL = value
        elif code == "ABS_HAT0Y":
            self.ABS_HAT0Y = value
        elif code == "ABS_HAT0X":
            self.ABS_HAT0X = value

    def toString(self):
        rj_msg = "ABS_RY:" + str(self.ABS_RY) + ",ABS_RX:" + str(self.ABS_RX) + ",BTNTHUMBR:" + str(self.BTN_THUMBR)
        lj_msg = ",ABS_Y:" + str(self.ABS_Y) + ",ABS_X:" + str(self.ABS_X) + ",BTNTHUMBL:" + str(self.BTN_THUMBL)
        hat_msg = ",ABS_HAT0Y:" + str(self.ABS_HAT0Y) + ",ABS_HAT0X:" + str(self.ABS_HAT0X)
        return rj_msg + lj_msg + hat_msg

    def notifyAll(self, msg):
        self.observer.sendOrders(msg)

    def Loop(self):
        while True:
            events = self.gamepad.read()
            for event in events:
                self.updateCommands(event.code, event.state)
                self.notifyAll(self.toString())
                print(self.toString())
