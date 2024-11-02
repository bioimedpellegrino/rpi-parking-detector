import os
import time
from picamera2 import Picamera2
from datetime import datetime

class Detector:
    def __init__(self):
        self.camera = Picamera2()
        self.media_dir = os.path.join('..', 'media')
        os.makedirs(self.media_dir, exist_ok=True)
    
    def close(self):
        if self.camera:
                self.camera.close()
                print("Camera chiusa")
        
    def take_snapshot(self) -> str:
        # Genera un nome file unico basato su data e ora
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        file_name = f'snapshot_{timestamp}.jpg'
        file_path = os.path.join(self.media_dir, file_name)

        # Scatta la foto e salva
        self.camera.start()
        time.sleep(1)
        self.camera.capture_file(file_path)
        self.camera.stop()

        return file_name
