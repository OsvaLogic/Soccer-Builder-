@echo off
title Iniciar Soccer Builder
echo ===================================================
echo        INICIANDO SOCCER BUILDER (DJANGO)
echo ===================================================

cd /d "%~dp0"

:: 1. Comprobar y crear entorno virtual si no existe
if not exist "venv\Scripts\activate.bat" (
    echo [!] No se encontro el entorno virtual. Creando uno nuevo...
    python -m venv venv
)

:: 2. Activar entorno virtual
echo [*] Activando entorno virtual...
call venv\Scripts\activate.bat

:: 3. Instalar requerimientos (si existe el archivo)
if exist requirements.txt (
    echo [*] Verificando dependencias...
    pip install -r requirements.txt -q
)

:: 4. Aplicar migraciones pendientes
echo [*] Aplicando migraciones a la base de datos...
python manage.py makemigrations
python manage.py migrate

:: 4.5 Poblar Base de Datos con Formaciones
echo [*] Verificando e inyectando tacticas en la BD...
python seed_formations.py

:: 5. Iniciar el servidor y abrir el navegador
echo [*] Levantando el servidor local en http://127.0.0.1:8000/
start http://127.0.0.1:8000/
python manage.py runserver

pause