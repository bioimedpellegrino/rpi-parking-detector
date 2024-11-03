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
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
IMAGE_NAME = 'parking.jpg'
BOXES_PATH = os.path.join(CONFIG_DIR, 'boxes.txt')

if __name__ == '__main__':
    detector = Detector(yolo_model=YOLO_MODEL, media_dir=MEDIA_DIR, image_name=IMAGE_NAME, boxes_file_path=BOXES_PATH)
    camera = RaspiCamera(MEDIA_DIR, 10)
    bot = TelegramBot(camera=camera, detector=detector)
    # Run the camera thread in a different thread --> this will take the snapshot every 10 seconds of the parking lot
    camera_thread = threading.Thread(target=camera.run)
    camera_thread.start()
    # Run the bot in the main thread (necessary because idle only works in the main thread)
    bot.run()
