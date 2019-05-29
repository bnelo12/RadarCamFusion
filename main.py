from threading import Thread
from flask import Flask

import eventlet
eventlet.monkey_patch()

from src.ObjectDetector import ObjectDetector as OD

def run_object_detection():
    from picamera import PiCamera
    from picamera.array import PiRGBArray

    IM_WIDTH = 1280
    IM_HEIGHT = 720

    print("Setting up neural network")
    od = OD()
    print("Neural network set up complete")

    camera = PiCamera()
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)

    print('Camera is now recording')
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        print("Detecting objects!")
        boxes, scores, classes, num = od.detect(frame)
        print(boxes)
        rawCapture.truncate(0)

    camera.close()

object_detection_thread = Thread(target=run_object_detection)
object_detection_thread.start()