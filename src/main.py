import os

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
    detector = Detector(YOLO_MODEL, BASE_DIR, MEDIA_DIR, TEST_IMAGE, BOXES_PATH)
    bot = TelegramBot(detector)
    raspi_camera = RaspiCamera(MEDIA_DIR, 10)
    while True:
        bot.run()
        raspi_camera.run()