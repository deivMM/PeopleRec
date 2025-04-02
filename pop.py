import cv2
import numpy as np
from ultralytics import YOLO
from datetime import datetime
import time
import os
import subprocess
import threading
import re

def get_image_path(base_dir="images"):
    today = datetime.today()
    year = str(today.year)
    month = f'{today.month:02d}'
    day = f'{today.day:02d}'
    image_path = os.path.join(os.getcwd(),base_dir, year, month, day)º
    os.makedirs(image_path, exist_ok=True)
    return image_path

def ejecutar_en_horario(func, start_hour, end_hour, start_minute=0, end_minute=0, interval=5):
    """
    Ejecuta una función en un hilo dentro del horario especificado.
    """
    global stop_detection

    start_time = datetime.strptime(f"{start_hour}:{start_minute}", "%H:%M").time()
    end_time = datetime.strptime(f"{end_hour}:{end_minute}", "%H:%M").time()

    thread = None  # Para manejar el hilo de ejecución
    running = False  # Bandera para saber si la cámara está encendida

    while True:
        now = datetime.now().time()
        print('-----------------', now, '-----------------')
        if now.minute % 2 == 0:
            if not running:
                print("Iniciando proceso de detección...")
                stop_detection = False
                thread = threading.Thread(target=func, daemon=True)
                thread.start()
                running = True
        else:
            if running:
                print("Fuera del horario. Cerrando proceso de detección...")
                stop_detection = True
                thread.join()
                running = False
        
        time.sleep(interval)  # Comprobación más frecuente

def main():
    image_path = get_image_path('app/static/images')

    exp_t = 3
    subprocess.run("v4l2-ctl --set-ctrl=auto_exposure=1", shell=True)
    subprocess.run(f"v4l2-ctl --set-ctrl=exposure_time_absolute={exp_t}", shell=True)

    print_web_cam_info = False

    if print_web_cam_info:
        resultado = subprocess.run('v4l2-ctl --list-ctrls', shell=True, capture_output=True, text=True)
        print("Salida:")
        print(resultado.stdout)

    tiempo_espera = 3
    ultimo_tiempo_deteccion = 0


    coco_model = YOLO("models/yolov8n.pt")
    COCO_LABELS = coco_model.names

    cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*'MJPG'))

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)


    if not cap.isOpened():
        print("Error: no se puede acceder a la cámara.")
        exit()

    # Crear la ventana solo una vez antes del bucle
    cv2.namedWindow('Cámara Web', cv2.WINDOW_NORMAL)

    mult = .7
    cv2.resizeWindow("Cámara Web", int(1920*mult), int(1080*mult))

    ret, frame = cap.read()

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    rect_container_limits = (900, 200, 1600, 900) # (x1, y1, x2, y2)
    mask = None # None cv2.imread('mask.png')
    object_to_detect = 'person' # None 'person' 'vehicle'

    if ret:
        h, w = frame.shape[:2]
        print(f"Alto (h): {frame_height}, Ancho (w): {frame_width}")


    filenames =[f for f in os.listdir(image_path) if f.endswith('jpg')]

    if filenames:
        pattern = r"img_(\d+)"
        numbers = [int(re.search(pattern, filename).group(1)) for filename in filenames]
        person_num = max(numbers)+1
    else:
        person_num = 1

    y_line = 300
    x_line = 350

    rect_container_limits = [250, 200, 450, 400] # x1, y1, x2, y2

    frame_width = 700
    frame_height = 700
    global stop_detection
    while not stop_detection:  
        ret, frame = cap.read()  # Leer un frame
        frame = frame[200:900, 900:1600]
        if not ret:  # Si no se pudo leer (final del video), salir del bucle
            break        
            
        if mask is not None:
            frame_with_mask = cv2.bitwise_and(frame, mask)
            results = coco_model(frame_with_mask)[0]
        else:
            results = coco_model(frame)[0]
        
        now = datetime.now()
        
        overlay = frame.copy()
        cv2.rectangle(overlay, (int(frame_width * 0.6), int(frame_height * 0.95)), 
                        (frame_width, frame_height), (100, 100, 100), -1)

        alpha = 0.5
        frame = cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0)
        
        timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

        cv2.putText(frame, timestamp, (int(frame_width * 0.6), int(frame_height * 0.97)), 
                    cv2.FONT_HERSHEY_SIMPLEX, .75, (0, 0, 0), 2)
        
        if len(results) == 0:
            pass
        else:
            for det in results.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = det
                object_name = COCO_LABELS[int(class_id)] if int(class_id) < len(COCO_LABELS) else "Unknown"
                if object_name in object_to_detect and score > 0.5 :
                    cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
                    text_x = int((x1 + x2) // 2)
                    text_y = int((y1 + y2) // 2)
                    
                    if rect_container_limits[0] <= text_x <= rect_container_limits[2] and rect_container_limits[1] <= text_y <= rect_container_limits[3]:
                        tiempo_actual = time.time()
                        if tiempo_actual - ultimo_tiempo_deteccion > tiempo_espera:
                            formatted_time = now.strftime("%H_%M_%S")
                            image_n = f'img_{person_num}__{formatted_time}'
                            print('imagen guardada')
                            cv2.imwrite(f'{image_path}/{image_n}.jpg', frame)
                            person_num += 1
                            ultimo_tiempo_deteccion = tiempo_actual

        
        cv2.rectangle(frame, (rect_container_limits[0], rect_container_limits[1]),
        (rect_container_limits[2], rect_container_limits[3]), (255, 0, 0), 5)

        # Mostrar el fotograma en la ventana previamente creada
        cv2.imshow('Cámara Web', frame)
        
        time.sleep(0.5)

        # Esperar a que se presione una tecla. Si es 'Q' o 'q', salir del bucle.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Liberar la cámara y cerrar todas las ventanas
    print("Cerrando cámara...")
    cap.release()
    cv2.destroyAllWindows()
    print("Camaras cerradas...")

ejecutar_en_horario(main, start_hour=8, end_hour=19, start_minute=0, end_minute=0, interval=10)
