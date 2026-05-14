# Archivo: upload_to_github.py
# Etiqueta: Script para subir el proyecto a GitHub automáticamente

import subprocess
import sys
import os
import shutil

# Colores para la interfaz de consola
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_step(message):
    print(f"\n{Colors.CYAN}{Colors.BOLD}➤ {message}{Colors.END}")

def run_command(command, hide_output=False):
    print(f"{Colors.BLUE}Ejecutando: {command}{Colors.END}")
    result = subprocess.run(command, shell=True, text=True, capture_output=True)
    
    if result.returncode != 0:
        print(f"{Colors.FAIL}❌ Error detectado:\n{result.stderr}{Colors.END}")
        return False
    else:
        if not hide_output and result.stdout.strip():
            print(result.stdout.strip())
        print(f"{Colors.GREEN}✔️ Completado{Colors.END}")
        return True

def check_gitignore():
    """Crea un .gitignore automáticamente si no existe para evitar subir basura o credenciales."""
    gitignore_content = """# Entornos virtuales
venv/
env/

# Variables de entorno
.env

# Base de datos SQLite
db.sqlite3

# Python cache
__pycache__/
*.pyc
"""
    if not os.path.exists(".gitignore"):
        print_step("Creando archivo .gitignore para proteger archivos sensibles...")
        with open(".gitignore", "w", encoding="utf-8") as f:
            f.write(gitignore_content)
        print(f"{Colors.GREEN}✔️ .gitignore creado exitosamente.{Colors.END}")

def main():
    print(f"{Colors.HEADER}{Colors.BOLD}=========================================")
    print("🚀 GITHUB UPLOADER - SOCCER BUILDER 🚀")
    print(f"========================================={Colors.END}\n")

    if shutil.which("git") is None:
        print(f"{Colors.FAIL}❌ Error: Git no está instalado o no está configurado en las variables de entorno.{Colors.END}")
        sys.exit(1)

    REPO_URL = "https://github.com/OsvaLogic/Soccer-Builder-.git"
    
    # Detectar si queremos forzar la fecha de ayer
    date_flag = ""
    if "--yesterday" in sys.argv:
        sys.argv.remove("--yesterday")
        date_flag = ' --date="yesterday"'

    if len(sys.argv) > 1:
        # Permite al usuario escribir el mensaje sin necesidad de usar comillas
        commit_message = " ".join(sys.argv[1:])
    else:
        commit_message = input(f"{Colors.WARNING}Ingresa el mensaje para el commit (ej. 'v.1.3' o 'Mejora en interfaz'): {Colors.END}").strip()
        if not commit_message:
            commit_message = "Actualización del proyecto"

    print_step("Inicializando repositorio Git...")
    run_command("git init")
    
    # Proteger credenciales y entorno virtual antes de hacer el 'git add .'
    check_gitignore()

    print_step("Añadiendo archivos...")
    run_command("git add .")
    
    print_step("Creando commit...")
    run_command(f'git commit -m "{commit_message}"{date_flag}')
    
    print_step("Preparando la rama principal y vinculando remoto...")
    run_command("git branch -M main")
    run_command(f"git remote set-url origin {REPO_URL} || git remote add origin {REPO_URL}")
    
    print_step("Subiendo cambios a GitHub...")
    success = run_command("git push -u origin main")
    
    if success:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ¡Proyecto subido exitosamente a GitHub! 🎉{Colors.END}")
    else:
        print(f"\n{Colors.FAIL}{Colors.BOLD}⚠️ Hubo problemas al subir el proyecto. Revisa los errores.{Colors.END}")

if __name__ == '__main__':
    main()