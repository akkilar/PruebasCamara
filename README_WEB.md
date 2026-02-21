# Monitor de Personas - RTSP

Sistema web de detección de personas en tiempo real mediante cámara RTSP using YOLO v8.

## Requisitos

- Python 3.8+
- Conexión a la cámara RTSP en la red local

## Instalación

1. Instala las dependencias:
```bash
pip install -r requirements.txt
```

2. Configura las credenciales en `app.py`:
   - `USUARIO`: Usuario de la cámara
   - `PASSWORD`: Contraseña de la cámara
   - `IP_CAMARA`: IP de la cámara en la red

## Uso

### Desde PC (escritorio):

```bash
python app.py
```

Luego abre en el navegador: `http://localhost:5000`

### Desde Tablet/Móvil en la misma red:

1. Encuentra la IP de tu PC en Windows:
   ```bash
   ipconfig
   ```
   Busca la dirección IPv4 de tu tarjeta de red local (ej: 192.168.1.100)

2. En la tablet, abre el navegador y ve a: `http://192.168.1.100:5000`

## Características

✅ Stream de video en tiempo real desde la cámara RTSP
✅ Contador de personas detectadas
✅ Alertas visuales cuando faltan personas
✅ Interfaz responsiva (funciona en desktop, tablet y móvil)
✅ Configuración de personas esperadas desde la web
✅ Actualización en tiempo real del estado

## Estructura

```
PruebasCamara/
├── app.py                 # Servidor Flask
├── requirements.txt       # Dependencias Python
├── templates/
│   └── index.html        # Interfaz web
├── ReadCamara.py         # Script original (opcional)
└── yolov8n.pt           # Modelo YOLO pre-entrenado
```

## Notas

- Mantén el programa corriendo en tu PC para que la tablet pueda acceder
- Asegúrate de que tablet y PC están en la misma red WiFi
- El álbum necesita estar en la red local (no funciona remotamente sin VPN)
- Para parar el servidor: presiona `Ctrl+C` en la terminal

## Solución de problemas

**"No se puede conectar a la cámara"**
- Verifica la IP, usuario y contraseña
- Prueba que la cámara es accesible desde tu red

**"No se ve el video desde la tablet"**
- Verifica la IP de tu PC (ipconfig)
- Asegúrate que la tablet y PC están en la misma red
- Desactiva firewall temporalmente para pruebas

**Video lento o entrecortado**
- Reduce el CPU usado: baja la calidad del modelo a `yolov8n.pt` (ya está)
- Aumenta el tamaño de frame: modifica `(1280, 720)` a `(640, 480)`
