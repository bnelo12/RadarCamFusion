import io

from picamera import PiCamera
from picamera.array import PiRGBArray

from src import socketio
from src.ObjectDetector import ObjectDetector as OD
import src.utils.radar as R

vision_thread = None
radar_thread = None

def capture(camera, rawCapture):
    for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        yield frame

def run_radar():
    while True:
        try:
            dataOk, _, detObj = R.update()
            if dataOk:
                data = {
                    'x': detObj['x'].tolist(),
                    'y': detObj['y'].tolist()
                }
                socketio.emit('range_data', data, broadcast=True)    
            socketio.sleep(0.033) # Sampling frequency of 30 Hz
            
        except KeyboardInterrupt:
            CLIport.write(('sensorStop\n').encode())
            CLIport.close()
            Dataport.close()
            win.close()
            break

def run_object_detection():
    IM_WIDTH = 1280
    IM_HEIGHT = 720
    od = OD()
    camera = PiCamera()
    camera.rotation = 270
    camera.resolution = (IM_WIDTH,IM_HEIGHT)
    camera.framerate = 10
    rawCapture = PiRGBArray(camera, size=(IM_WIDTH,IM_HEIGHT))
    rawCapture.truncate(0)
    jpg_capture = io.BytesIO()
    camera.capture(jpg_capture, 'jpeg')
    for frame in capture(camera, rawCapture):
        camera.resolution = (1280,720)
        camera.capture(jpg_capture, 'jpeg')
        camera.resolution = (IM_WIDTH,IM_HEIGHT)
        boxes, scores, classes, num = od.detect(frame)
        data = {    
            'image': jpg_capture.getvalue(),
            'boxes': boxes[0].tolist(),
            'scores': scores.tolist(),
            'classes': classes[0].tolist()
        }
        socketio.emit('image', data, broadcast=True)
        jpg_capture = io.BytesIO()
        rawCapture.truncate(0)
        socketio.sleep(0)

    camera.close()

@socketio.on('connect')
def on_connect():
    global vision_thread
    global radar_thread
    print('Client connected')
    if vision_thread is None:
        vision_thread = socketio.start_background_task(run_object_detection)
    if radar_thread is None:
        radar_thread = socketio.start_background_task(run_radar)
    return