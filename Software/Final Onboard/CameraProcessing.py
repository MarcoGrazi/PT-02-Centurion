from picamera import PiCamera
from time import sleep
import time

class CameraProcessing:
    def __init__(self):
        #self.rec = 0
        #self.camera = PiCamera()
        #self.camera.resolution = (768, 1024)
        #self.camera.framerate = 30
        #TODO: explore settings for
        print("CameraSetup")

    def Record(self):
        print("rec")
        #if self.rec:
         #   self.camera.stop_recording()
          #  self.camera.stop_preview()
           # self.rec = 0
            #print("stopped")
        #else:
         #   self.camera.start_preview()
          #  self.camera.start_recording("/home/pi/Desktop" + time.strftime("%M%S")+".h264")
           # self.rec = 1
            #print("rec")