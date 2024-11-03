import os
import json
import cv2

from ultralytics import YOLO


class Detector:
    
    def __init__(self, media_dir: str, yolo_model: str, image_name: str, boxes_file_path: str):
        self.media_dir = media_dir
        self.yolo_model = YOLO(yolo_model)
        self.image_name = image_name 
        self.boxes_to_monitor = []
        self.cars_center_points = []
        self.free_boxes = {}
        self.situation_path = None
        if boxes_file_path and os.path.exists(boxes_file_path):
            with open(boxes_file_path, 'r') as json_file:
                self.boxes_to_monitor = json.load(json_file)
    
    def is_point_in_area(self, point, area):
        x1, y1 = area[0] # Start point
        x2, y2 = area[1] # End point
        return x1 <= point[0] <= x2 and y1 <= point[1] <= y2
    
    def detect(self):
        
        image_path = os.path.join(self.media_dir, self.image_name)
        results = self.yolo_model.predict(image_path)
        
        for result in results:
            for detected in result.boxes:
                label = int(detected.cls[0])
                if label == 2:  # La label delle "auto" secondo COCO
                    x1, y1, x2, y2 = map(int, detected.xyxy[0])
                    center_x = (x1 + x2) // 2
                    center_y = (y1 + y2) // 2
                    center_point = (center_x, center_y)
                    self.cars_center_points.append(center_point)
                    
    def check_free_spot(self):
        for box in self.boxes_to_monitor:
            area = (box["start_point"], box["end_point"])
            for center_point in self.cars_center_points:
                if self.is_point_in_area(center_point, area):
                    box['is_occupied'] = True
                    break
            else:
                self.free_boxes[box['id']] = (box["start_point"], box["end_point"])
        
        self.draw_and_save_boxes()
                
    def draw_and_save_boxes(self):

        image_path = os.path.join(self.media_dir, self.image_name)
        output_path = os.path.join(self.media_dir, "situation.jpg")

        image = cv2.imread(image_path)
        
        color_free = (0, 255, 0)
        color_occupied = (0, 0, 255)

        for box in self.boxes_to_monitor:
            start_point = tuple(box["start_point"])
            end_point = tuple(box["end_point"])
            color = color_occupied if box['is_occupied'] else color_free
            cv2.rectangle(image, start_point, end_point, color, 2)  # 2 è lo spessore della linea

        cv2.imwrite(output_path, image)

        self.situation_path =  output_path