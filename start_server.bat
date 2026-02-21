@echo off
echo.
echo ====================================================
echo   Monitor de Personas - Servidor Web
echo ====================================================
echo.

REM Verificar si Flask está instalado
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo Error instalando dependencias
        pause
        exit /b 1
    )
)

echo.
echo ✓ Iniciando servidor...
echo.
echo Acceso desde PC:     http://localhost:5000
echo.
echo Para acceder desde tablet:
echo   1. Abre terminal: ipconfig
echo   2. Busca IPv4 (ej: 192.168.x.x)
echo   3. En tablet: http://192.168.x.x:5000
echo.
echo Presiona Ctrl+C para detener el servidor
echo ====================================================
echo.

python app.py

pause
