import cv2
from ultralytics import YOLO

# 1. Configuración de acceso
USUARIO = 'tu_usuario_tapo'
PASSWORD = 'tu_password_tapo'
IP_CAMARA = '192.168.1.XX' # Cambia por la IP real

# URL RTSP para la Tapo C200 (stream1 es alta calidad, stream2 es baja)
rtsp_url = f"rtsp://{USUARIO}:{PASSWORD}@{IP_CAMARA}:554/stream1"

# 2. Cargar el modelo YOLO (n = nano, el más rápido para tiempo real)
model = YOLO('yolov8n.pt') 

# 3. Iniciar captura de video
cap = cv2.VideoCapture(rtsp_url)

if not cap.isOpened():
    print("Error: No se pudo conectar a la cámara. Revisa IP y credenciales.")
    exit()

print("Conectado. Presiona 'q' para salir.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # 4. Ejecutar detección (solo clase 0 que es 'persona' en COCO dataset)
    results = model(frame, classes=[0], conf=0.5, verbose=False)

    # 5. Dibujar resultados en la imagen
    annotated_frame = results[0].plot()

    # Mostrar el frame con la detección
    cv2.imshow("Detección de Personas - Tapo C200", annotated_frame)

    # Salir con la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()