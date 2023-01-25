import serial

class SerialTransmitter:
    def __init__(self, address):
        self.antenna = serial.Serial(port=address, baudrate=11520, timeout=1)

    def sendOrders(self, msg):
        self.antenna.open()
        self.antenna.write(msg)
        self.antenna.close()
        print("sent")
