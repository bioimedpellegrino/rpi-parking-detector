import cv2
import json
import os

from ultralytics import YOLO
from dotenv import load_dotenv
load_dotenv()

YOLO_MODEL = os.getenv('YOLO_MODEL')
BASE_DIR = os.getenv('BASE_DIR')
MEDIA_DIR = os.path.join(BASE_DIR, 'media')
TEST_IMAGE = 'test_park.jpg'
BOXES_PATH = os.path.join(MEDIA_DIR, 'boxes.txt')
model = YOLO(YOLO_MODEL)

image_path = os.path.join(MEDIA_DIR, TEST_IMAGE)
frame = cv2.imread(image_path)

with open(BOXES_PATH, 'r') as json_file:
    boxes = json.load(json_file)

def is_point_in_area(point, area):
    x1, y1 = area[0] # Start point
    x2, y2 = area[1] # End point
    return x1 <= point[0] <= x2 and y1 <= point[1] <= y2

results = model.predict(frame)

free_boxes = []
cars_center_points = []
print(f"Numero box da monitorare {len(boxes)}")

for result in results:
    for detected in result.boxes:
        label = int(detected.cls[0])
        if label == 2:  # La label delle "auto" secondo COCO
            x1, y1, x2, y2 = map(int, detected.xyxy[0])
            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            center_point = (center_x, center_y)
            cars_center_points.append(center_point)
            
for box in boxes:
    area = (boxes[box]["start_point"], boxes[box]["end_point"])
    for center_point in cars_center_points:
        if is_point_in_area(center_point, area):
            boxes[box]['is_occupied'] = True
            break
    else:
        free_boxes.append(boxes[box])

for box in boxes:
    start_point = boxes[box]["start_point"]
    end_point = boxes[box]["end_point"]
    color = (0, 0, 255) if boxes[box]['is_occupied'] else (0, 255, 0)
    cv2.rectangle(frame, start_point, end_point, color, 2)
    
cv2.imshow('Output', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f'Free boxes: {free_boxes}')
