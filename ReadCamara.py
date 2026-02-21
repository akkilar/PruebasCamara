import cv2
from ultralytics import YOLO
import numpy as np

# 1. Configuración de acceso
USUARIO = 'akkilar'
PASSWORD = 'Hyperion2025'
IP_CAMARA = '192.168.3.149' # Cambia por la IP real

# 2. Configuración de detección de personas
PERSONAS_ESPERADAS = 2  # Número de personas que debería haber en la cámara

# URL RTSP para la Tapo C200 (stream1 es alta calidad, stream2 es baja)
rtsp_url = f"rtsp://{USUARIO}:{PASSWORD}@{IP_CAMARA}:554/stream1"

# 3. Cargar el modelo YOLO (n = nano, el más rápido para tiempo real)
model = YOLO('yolov8n.pt') 

# 4. Iniciar captura de video
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: No se pudo conectar a la cámara. Revisa IP y credenciales.")
    exit()

print("Conectado. Presiona 'q' para salir.")
print(f"Esperando {PERSONAS_ESPERADAS} persona(s) en la cámara...")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar la imagen a un tamaño fijo (ej: 800x600)
    frame_pequeno = cv2.resize(frame, (1280, 720))

    # 5. Ejecutar detección (solo clase 0 que es 'persona' en COCO dataset)
    results = model(frame_pequeno, classes=[0], conf=0.5, verbose=False)

    # 6. Contar personas detectadas
    num_personas = len(results[0].boxes)

    # 7. Dibujar resultados en la imagen
    annotated_frame = results[0].plot()

    # 8. Mostrar contador de personas detectadas
    texto_contador = f"Personas detectadas: {num_personas}/{PERSONAS_ESPERADAS}"
    color_texto = (0, 255, 0) if num_personas >= PERSONAS_ESPERADAS else (0, 0, 255)
    cv2.putText(annotated_frame, texto_contador, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color_texto, 2)

    # 9. Mostrar aviso si hay menos personas de las esperadas
    if num_personas < PERSONAS_ESPERADAS:
        # Mostrar banner de alerta
        alerta_texto = f"¡ALERTA! Faltan {PERSONAS_ESPERADAS - num_personas} persona(s)"
        cv2.rectangle(annotated_frame, (0, 50), (annotated_frame.shape[1], 100), (0, 0, 255), -1)
        cv2.putText(annotated_frame, alerta_texto, (10, 85), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (255, 255, 255), 3)
        print(f"⚠️  ALERTA: {alerta_texto}")

    # Mostrar el frame con la detección
    cv2.imshow("Deteccion de Personas - Tapo C200", annotated_frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()