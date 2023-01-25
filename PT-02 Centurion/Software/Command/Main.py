from Command.OrderGenerator import OrderGenerator
from Command.SerialTransmitter import SerialTransmitter
import threading

ARDUINO_ADDRESS = "COM13"

ST = SerialTransmitter(ARDUINO_ADDRESS)

order_generator = OrderGenerator(ST)
t_orders = threading.Thread(target=order_generator.Loop)
t_orders.daemon = True
t_orders.start()

while True:
    pass
