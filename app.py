import cv2
from ultralytics import YOLO
from flask import Flask, render_template, Response, jsonify
import threading
import time
import torch

# Permitir cargar modelos de YOLO con PyTorch 2.6+
torch.serialization.add_safe_globals([torch.Tensor])
try:
    from ultralytics.nn.tasks import DetectionModel
    torch.serialization.add_safe_globals([DetectionModel])
except:
    pass

app = Flask(__name__)

# Configuración
USUARIO = 'akkilar'
PASSWORD = 'Hyperion2025'
IP_CAMARA = '192.168.3.149'
PERSONAS_ESPERADAS = 2

rtsp_url = f"rtsp://{USUARIO}:{PASSWORD}@{IP_CAMARA}:554/stream1"

# Variables globales
model = YOLO('yolov8n.pt')
cap = None
num_personas_actual = 0
alerta_activa = False
lock = threading.Lock()

def inicializar_camara():
    """Inicializa la conexión con la cámara"""
    global cap
    cap = cv2.VideoCapture(rtsp_url)
    if not cap.isOpened():
        print("Error: No se pudo conectar a la cámara")
        return False
    print("Conectado a la cámara")
    return True

def generar_frames():
    """Genera frames para streaming"""
    global num_personas_actual, alerta_activa
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error leyendo frame")
            break
        
        # Redimensionar
        frame = cv2.resize(frame, (1280, 720))
        
        # Detección YOLO
        results = model(frame, classes=[0], conf=0.5, verbose=False)
        
        with lock:
            num_personas_actual = len(results[0].boxes)
            alerta_activa = num_personas_actual < PERSONAS_ESPERADAS
        
        # Dibujar resultados
        annotated_frame = results[0].plot()
        
        # Mostrar contador
        alto, ancho = annotated_frame.shape[:2]
        texto_contador = f"Personas: {num_personas_actual}/{PERSONAS_ESPERADAS}"
        if num_personas_actual >= PERSONAS_ESPERADAS:
            color_texto = (0, 255, 0) 
            grosor = 3
        else: 
            color_texto = (0, 0, 255)
            grosor = 2
        cv2.putText(annotated_frame, texto_contador, (10, alto - 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color_texto, grosor)
        
        # Mostrar alerta si es necesario
        if alerta_activa:
            alerta_texto = f"¡ALERTA! Faltan {PERSONAS_ESPERADAS - num_personas_actual} persona(s)"
            cv2.rectangle(annotated_frame, (0, alto - 45), (ancho, alto), (0, 0, 255), -1)
            cv2.putText(annotated_frame, alerta_texto, (10, alto - 15), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        
        # Codificar frame
        ret, buffer = cv2.imencode('.jpg', annotated_frame)
        frame_bytes = buffer.tobytes()
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n'
               b'Content-Length: ' + str(len(frame_bytes)).encode() + b'\r\n\r\n' + frame_bytes + b'\r\n')

@app.route('/')
def index():
    """Página principal"""
    return render_template('index.html', personas_esperadas=PERSONAS_ESPERADAS)

@app.route('/video_feed')
def video_feed():
    """Stream de video"""
    return Response(generar_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/status')
def status():
    """Retorna el estado actual"""
    with lock:
        return jsonify({
            'personas': num_personas_actual,
            'esperadas': PERSONAS_ESPERADAS,
            'alerta': alerta_activa
        })

@app.route('/config/<int:personas>')
def config(personas):
    """Cambia el número de personas esperadas"""
    global PERSONAS_ESPERADAS
    if 1 <= personas <= 20:
        PERSONAS_ESPERADAS = personas
        return jsonify({'success': True, 'personas': PERSONAS_ESPERADAS})
    return jsonify({'success': False, 'error': 'Número inválido'}), 400

if __name__ == '__main__':
    if inicializar_camara():
        # Iniciar el servidor Flask
        app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)
    else:
        print("No se puede iniciar sin conexión a la cámara")
