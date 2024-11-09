import time
from picamera2 import Picamera2
import keyboard

picam2 = Picamera2()
config = picam2.create_still_configuration(lores={'size': (640, 480)}, display='lores', buffer_count=3)
picam2.configure(config)
picam2.start(show_preview=True)

print("Premi 'q' o 'ESC' per uscire...")

while True:
    if keyboard.is_pressed('q'):
        print("Hai premuto 'q'. Uscendo...")
        picam2.close()
        break
    elif keyboard.is_pressed('esc'):
        print("Hai premuto 'ESC'. Uscendo...")
        picam2.close()
        break
