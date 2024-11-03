import cv2
import json
import os

from dotenv import load_dotenv
load_dotenv()

BASE_DIR = os.getenv("BASE_DIR")
CONFIG_DIR = "config"
MEDIA_DIR = "media"
TEST_IMAGE = "parking.jpg"

drawing = False
start_point = None
indx = 0
boxes = []
boxes_path = os.path.join(BASE_DIR, CONFIG_DIR, "boxes.txt")

def draw_rectangle(event, x, y, flags, param):
    global drawing, start_point, boxes, indx
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_point = (x, y)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing and start_point:
            img_copy = frame.copy()
            cv2.rectangle(img_copy, start_point, (x, y), (255, 0, 0), 2)
            cv2.imshow('Draw Parking Boxes', img_copy)

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        indx += 1
        end_point = (x, y)
        boxes.append({"id": indx, "start_point": start_point, "end_point": end_point, "is_occupied": False})
        cv2.rectangle(frame, start_point, end_point, (255, 0, 0), 2)

image_path = os.path.join(BASE_DIR, MEDIA_DIR, TEST_IMAGE)
frame = cv2.imread(image_path)

cv2.namedWindow('Draw Parking Boxes')
cv2.setMouseCallback('Draw Parking Boxes', draw_rectangle)

while True:
    cv2.imshow('Draw Parking Boxes', frame)
    if cv2.waitKey(1) & 0xFF == 27: # ESC
        break

with open(boxes_path, 'w') as json_file:
    json.dump(boxes, json_file)

print("Boxes saved to config/boxes.txt")

cv2.destroyAllWindows()
