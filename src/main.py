import os
import threading

from detector import Detector
from bot import TelegramBot
from raspi_camera import RaspiCamera
from dotenv import load_dotenv
load_dotenv()

YOLO_MODEL = os.getenv('YOLO_MODEL')
BASE_DIR = os.getenv('BASE_DIR')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
TEST_IMAGE = 'test_park.jpg'
BOXES_PATH = os.path.join(MEDIA_DIR, 'boxes.txt')

if __name__ == '__main__':
    detector = Detector(yolo_model=YOLO_MODEL, media_dir=MEDIA_DIR, image_name=TEST_IMAGE, boxes_file_path=BOXES_PATH)
    camera = RaspiCamera(MEDIA_DIR, 10)
    bot = TelegramBot(camera=camera, detector=detector)
    camera_thread = threading.Thread(target=camera.run)
    camera_thread.start()
    camera_thread.join()
    
    bot.run()
