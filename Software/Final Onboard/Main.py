import threading
from OrderReceiver import OrderReceiver
from MotorController import MotorController
from CameraProcessing import CameraProcessing

CP = CameraProcessing()
MC = MotorController(CP)
OR = OrderReceiver(MC)

t_orders = threading.Thread(target=OR.Loop)
t_orders.daemon = True
t_orders.start()

while True:
    pass