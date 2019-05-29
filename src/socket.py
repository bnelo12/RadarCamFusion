from threading import Lock
from src import socketio
import io
import time
import base64

from picamera import PiCamera
from picamera.array import PiRGBArray

from src.ObjectDetector import ObjectDetector as OD

thread_lock = Lock()
thread = None
ready = True

def capture(camera, rawCapture):
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        yield frame

def run_object_detection():
    global ready
    IM_WIDTH = 1280
    IM_HEIGHT = 720

    print("Setting up neural network")
    od = OD()
    print("Neural network set up complete")

    camera = PiCamera()
    camera.rotation = 270
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)
    jpg_capture = io.BytesIO()
    camera.capture(jpg_capture, 'jpeg')
    print('Camera is now recording')
    for frame in capture(camera, rawCapture):
        ready = False
        camera.resolution = (160,90)
        camera.capture(jpg_capture, 'jpeg')
        camera.resolution = (IM_WIDTH,IM_HEIGHT)
        boxes, scores, classes, num = od.detect(frame)
        socketio.emit('image', jpg_capture.getvalue(), broadcast=True)
        jpg_capture = io.BytesIO()
        rawCapture.truncate(0)
        socketio.sleep(0)

    camera.close()

@socketio.on('connect')
def on_connect():
    global thread
    print('Client connected')
    if thread is None:
        thread = socketio.start_background_task(run_object_detection)
    return