from picamera2 import Picamera2
from libcamera import ColorSpace

class Camera():

    def __init__(self):
        self.camera = Picamera2()
        camera_config = self.camera.create_still_configuration({"size": (1920, 1080)})
        self.camera.configure(camera_config)
        self.camera.start() 
        
    def capture_image(self):
        return self.camera.capture_array()
    
    def stop_camera(self):
        self.camera.stop()