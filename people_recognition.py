from picamera2 import Picamera2
import cv2
from datetime import datetime
from ultralytics import YOLO
import os
import re
import time

picam2 = Picamera2()
picam2.preview_configuration.main.size = (1920, 1080)
picam2.preview_configuration.main.format = "RGB888"
picam2.configure("preview")
picam2.start()

frame = picam2.capture_array()
frame_height, frame_width, channels = frame.shape

image_path  = 'images_people_temp'
coco_model = YOLO("models/yolov8n.pt")
COCO_LABELS = coco_model.names

rect_container_limits = (.5, 0.3, .7, .6) # (x1, y1, x2, y2)
cropped_frame_limits = (.4, 0.15, .75, .7) # (x1, y1, x2, y2)


rect_container_limits = (int(rect_container_limits[0] * frame_width), int(rect_container_limits[1] * frame_height),
                        int(rect_container_limits[2] * frame_width), int(rect_container_limits[3] * frame_height))

tiempo_espera = 3
ultimo_tiempo_deteccion = 0

while True:
    frame = picam2.capture_array()
    
    results = coco_model(frame)[0]
    
    overlay = frame.copy()
    cv2.rectangle(overlay, (int(frame_width * 0.6), int(frame_height * 0.92)), 
                    (frame_width, frame_height), (100, 100, 100), -1)

    alpha = 0.5
    frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
    
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    cv2.putText(frame, timestamp, (int(frame_width * 0.62), int(frame_height * 0.97)), 
                cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 2)
    
    if len(results) == 0:
        pass
    else:
        for det in results.boxes.data.tolist():
            x1, y1, x2, y2, score, class_id = det
            object_name = COCO_LABELS[int(class_id)] if int(class_id) < len(COCO_LABELS) else "Unknown"
            if object_name in 'person' and score > 0.5 :
                cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                obj_x_coord = int((x1 + x2) // 2)
                obj_y_coord = int((y1 + y2) // 2)
                
                if rect_container_limits[0] <= obj_x_coord <= rect_container_limits[2] and rect_container_limits[1] <= obj_y_coord <= rect_container_limits[3]:
                    tiempo_actual = time.time()
                    if tiempo_actual - ultimo_tiempo_deteccion > tiempo_espera:
                        formatted_time = now.strftime("%Y_%m_%d__%H_%M_%S")
                        
                        cropped_frame = frame[int(cropped_frame_limits[1] * frame_height):int(cropped_frame_limits[3] * frame_height),
                                            int(cropped_frame_limits[0] * frame_width):int(cropped_frame_limits[2] * frame_width)]
                        
                        image_n = f'img_{formatted_time}'
                        print('imagen guardada')
                        cv2.imwrite(f'{image_path}/{image_n}.jpg', cropped_frame)
                        ultimo_tiempo_deteccion = tiempo_actual
        
    cv2.rectangle(frame, (rect_container_limits[0], rect_container_limits[1]),
                (rect_container_limits[2], rect_container_limits[3]),(255, 0, 0),2)
    
    cv2.rectangle(frame, (int(cropped_frame_limits[0] * frame_width), int(cropped_frame_limits[1] * frame_height)),
                (int(cropped_frame_limits[2] * frame_width), int(cropped_frame_limits[3] * frame_height)),(0, 0, 255),2)

    cv2.imshow("Frame", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
