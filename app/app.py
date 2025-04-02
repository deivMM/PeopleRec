from flask import Flask, render_template, request, jsonify, send_from_directory
import os
from datetime import datetime
import re

app = Flask(__name__)

# Ruta donde se almacenan las imágenes
IMAGE_DIR = "static/images"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_images/<year>/<month>/<day>')
def get_images(year, month, day):
    """Devuelve la lista de imágenes para la fecha seleccionada."""
    date_path = os.path.join(IMAGE_DIR, year, month, day)
    if not os.path.exists(date_path):
        return jsonify([])
    images = sorted(os.listdir(date_path))
    return jsonify(images)

@app.route('/contar_imagenes')
def contar_imagenes():
    fecha = request.args.get('fecha').replace('-', '/') 
    carpeta = os.path.join('static/images', fecha)

    if not os.path.exists(carpeta):
        return jsonify({'numero': 0})
    
    imagenes = [f for f in os.listdir(carpeta) if f.endswith(('.jpg', '.png', '.jpeg'))]
    return jsonify({'numero': len(imagenes)})


@app.route('/get-hora', methods=['POST'])
def get_hora():
    data = request.get_json()
    nombre_imagen = data.get('nombreImagen', '')

    match = re.search(r'(\d)__(\d{2})_(\d{2})_(\d{2})', nombre_imagen)
    if match:
        image_id = f"{match.group(1)}"
        hora = f"{match.group(2)}:{match.group(3)}:{match.group(4)}"
        return jsonify({'hora': hora, 'id': image_id})
    else:
        return jsonify({'hora': '---', 'id': '---'})


@app.route('/static/images/<year>/<month>/<day>/<filename>')
def serve_image(year, month, day, filename):
    """Sirve la imagen solicitada."""
    return send_from_directory(os.path.join(IMAGE_DIR, year, month, day), filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)

#    
# http://127.0.0.1:5001 → Es la dirección local (localhost)
# Solo puedes acceder a la web desde el mismo dispositivo donde está corriendo Flask.
#
# http://192.168.1.130:5001 → Es la dirección de red local (LAN).
# Cualquier otro dispositivo conectado a la misma red WiFi puede acceder.
#