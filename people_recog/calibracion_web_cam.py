import cv2
import subprocess

resultado = subprocess.run('v4l2-ctl --list-ctrls', shell=True, capture_output=True, text=True)

print("Salida:")
print(resultado.stdout)


subprocess.run("v4l2-ctl --set-ctrl=auto_exposure=1", shell=True)
subprocess.run("v4l2-ctl --set-ctrl=exposure_time_absolute=500", shell=True)

resultado = subprocess.run('v4l2-ctl --list-ctrls', shell=True, capture_output=True, text=True)

print("Salida:")
print(resultado.stdout)

cap = cv2.VideoCapture(0, cv2.CAP_V4L2)

# Forzar formato MJPG para poder usar 1920x1080
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
if ret:
    h, w = frame.shape[:2]
    print(f"Alto (h): {h}, Ancho (w): {w}")


while True:
    # Leer un fotograma de la cámara
    ret, frame = cap.read()

    if not ret:
        print("Error: no se pudo obtener un fotograma.")
        break

    # Mostrar el fotograma en la ventana previamente creada
    cv2.imshow('Cámara Web', frame)

    # Esperar a que se presione una tecla. Si es 'Q' o 'q', salir del bucle.
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la cámara y cerrar todas las ventanas
cap.release()
cv2.destroyAllWindows()
