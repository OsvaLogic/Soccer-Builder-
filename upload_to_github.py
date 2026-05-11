# Archivo: upload_to_github.py
# Etiqueta: Script para subir el proyecto a GitHub automáticamente

import subprocess
import sys

def run_command(command):
    print(f"Ejecutando: {command}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    if result.returncode != 0:
        print(f"Error detectado:\n{result.stderr}")
    else:
        print(result.stdout)
        print("✔️ Completado\n")

def main():
    # ⚠️ REEMPLAZA ESTA URL CON LA DE TU REPOSITORIO EN GITHUB
    REPO_URL = "https://github.com/OsvaLogic/Soccer-Builder-.git"
    
    if REPO_URL == "https://github.com/tu-usuario/soccer-builder.git":
        print("Por favor, edita este script y coloca la URL real de tu repositorio en la variable REPO_URL.")
        sys.exit(1)

    run_command("git init")
    run_command("git add .")
    run_command('git commit -m "v.1.2"')
    run_command("git branch -M main")
    # Intenta actualizar el remoto si ya existe, si falla, lo añade
    run_command(f"git remote set-url origin {REPO_URL} || git remote add origin {REPO_URL}")
    run_command("git push -u origin main")

if __name__ == '__main__':
    main()