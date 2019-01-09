import picamera
import time
import os

def take_picture(filename):
    camera = picamera.PiCamera()
    camera.start_preview()
    # Wait a few seconds to allow the lens time to adjust to the current light levels.
    time.sleep(5)
    camera.capture('./photos/%s.jpg' % filename)
    camera.stop_preview()
    print('Image %s.jpg saved' % filename)


def clear_photos_folder():
    for file in os.listdir('./photos'):
        print(file)