# Archivo: upload_to_github.py
# Etiqueta: Script para subir el proyecto a GitHub automáticamente

import subprocess
import sys

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

def main():
    print(f"{Colors.HEADER}{Colors.BOLD}=========================================")
    print("🚀 GITHUB UPLOADER - SOCCER BUILDER 🚀")
    print(f"========================================={Colors.END}\n")

    REPO_URL = "https://github.com/OsvaLogic/Soccer-Builder-.git"
    
    if len(sys.argv) > 1:
        commit_message = sys.argv[1]
    else:
        commit_message = input(f"{Colors.WARNING}Ingresa el mensaje para el commit (ej. 'v.1.3' o 'Mejora en interfaz'): {Colors.END}").strip()
        if not commit_message:
            commit_message = "Actualización del proyecto"

    print_step("Inicializando repositorio Git...")
    run_command("git init")
    
    print_step("Añadiendo archivos...")
    run_command("git add .")
    
    print_step("Creando commit...")
    run_command(f'git commit -m "{commit_message}"')
    
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