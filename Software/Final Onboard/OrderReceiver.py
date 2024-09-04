import serial
from MotorController import Orders, MotorController
import time

class OrderReceiver:
    def __init__(self, observer):
        self.observer = observer
        self.antenna = serial.Serial("/dev/ttyUSB0", 9600, timeout=0.15)
        self.prev = time.time()
        
    def Decode(self, data):
        orders = Orders(49, 49, 49, 49, 1, 1, 0, 0)
        start = 0
        end = 0
        pointer = 0
        while start != -1 and end != -1:
            start = data.find(".", pointer)
            end = data.find(".", start+1)
            if start != -1 and end != -1:
                o = data[start+1:end]
                if len(o) >= 2:
                    orders.setOrder(o)
                pointer = end
        return orders

    def Loop(self):
        while True:
            msg = self.antenna.readline().decode()
            self.observer.executeOrders(self.Decode(msg))
               
            