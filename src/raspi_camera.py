import os
from picamera2 import Picamera2

from ultralytics import YOLO
from time import sleep

class RaspiCamera:
    def __init__(self, media_dir: str, sleep_seconds: int):
        self.camera = Picamera2()
        self.media_dir = media_dir
        self.sleep_seconds = sleep_seconds
        self.is_camea_active = False
    
    def deactivate(self):
        if self.camera:
            self.camera.close()
            print("Camera closed")
    
    def activate(self):
        self.is_camera_active = True
        self.camera.start()    
                        
    def take_snapshot(self) -> str:
        snapshot_name = 'parking.jpg'
        snapshot_path = os.path.join(self.media_dir, snapshot_name)
        sleep(1)
        self.camera.capture_file(snapshot_path)
        print("Raspi camera: snapshot taken")
        return snapshot_path
    
    def idle(self):
        sleep(self.sleep_seconds)
        
    def run(self):
        self.activate()
        while True:
            self.take_snapshot()
            self.idle()
        
