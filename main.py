from picamera import PiCamera
from picamera.array import PiRGBArray

from ObjectDetector import ObjectDetector as OD

IM_WIDTH = 1280
IM_HEIGHT = 720

od = OD()

camera = PiCamera()
camera.resolution = (IM_WIDTH,IM_HEIGHT)
camera.framerate = 10
rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
rawCapture.truncate(0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    boxes, scores, classes, num = od.detect(frame))
    rawCapture.truncate(0)

camera.close()

