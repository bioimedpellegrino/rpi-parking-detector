import cv2
import json
from ultralytics import YOLO

# Carica il modello YOLO
model = YOLO('yolov8n.pt')

# Leggi l'immagine
image_path = '../media/test_park.jpg'
frame = cv2.imread(image_path)

with open('rectangles.json', 'r') as json_file:
    rectangles = json.load(json_file)

def is_point_in_rectangle(point, rect):
    x1, y1 = rect[0]
    x2, y2 = rect[1]
    return x1 <= point[0] <= x2 and y1 <= point[1] <= y2

# Esegui la previsione con il modello
results = model.predict(frame)

car_boxes = []
occupied_rectangles = []
print(f"Numero box da monitorare {len(rectangles)}")

for result in results:
    for detected in result.boxes:
        label = int(detected.cls[0])
        print(label)
        if label == 2:  # La label delle "auto" secondo COCO
            x1, y1, x2, y2 = map(int, detected.xyxy[0])
            area = (x2 - x1) * (y2 - y1)
            car_boxes.append((x1, y1, x2, y2, area))
            #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            #cv2.putText(frame, f'Area: {area}', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

            center_x = (x1 + x2) // 2
            center_y = (y1 + y2) // 2
            center_point = (center_x, center_y)

            for idx, rect in enumerate(rectangles):
                if is_point_in_rectangle(center_point, rect):
                    occupied_rectangles.append(rect)
                    cv2.rectangle(frame, rect[0], rect[1], (0, 0, 255), 2)
                    break
            else:
                cv2.rectangle(frame, rect[0], rect[1], (0, 255, 0), 2)
        else:
                cv2.rectangle(frame, rect[0], rect[1], (0, 255, 0), 2)

for box in car_boxes:
    print(f'Box: {box[:4]}, Area: {box[4]}')

cv2.imshow('Detected Cars', frame)
cv2.waitKey(0)
cv2.destroyAllWindows()

print(f'Occupied Rectangles: {occupied_rectangles}')
