from picamera2 import Picamera2
import cv2
from datetime import datetime
from ultralytics import YOLO
import os
import re


picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

coco_model = YOLO("models/yolov8n.pt")
COCO_LABELS = coco_model.names

frame_width = 640
frame_height = 480

while True:
    frame = picam2.capture_array()
    
    results = coco_model(frame)[0]
    
    if len(results) == 0:
        pass
    else:
        for det in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = det
            object_name = COCO_LABELS[int(class_id)] if int(class_id) < len(COCO_LABELS) else "Unknown"
            if object_name in 'person' and score > 0.5 :
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (int(frame_width * 0.6), int(frame_height * 0.92)), 
                    (frame_width, frame_height), (100, 100, 100), -1)

    alpha = 0.5
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    cv2.putText(frame, timestamp, (int(frame_width * 0.62), int(frame_height * 0.97)), 
                cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 2)
    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break






# def get_image_path(base_dir="images"):
#     today = datetime.today()
#     year = str(today.year)
#     month = f'{today.month:02d}'
#     day = f'{today.day:02d}'
#     image_path = os.path.join(os.path.dirname(os.getcwd()),base_dir, year, month, day)
#     os.makedirs(image_path, exist_ok=True)
#     return image_path


# image_path = get_image_path('app/static/images')
# print(image_path)