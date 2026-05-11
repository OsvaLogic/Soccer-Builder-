import os
import django

# Configurar el entorno de Django para poder usar los modelos
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from teams.models import Formation

def run_seeder():
    print("=========================================")
    print("⚽ INICIANDO CARGA DE TÁCTICAS ⚽")
    print("=========================================")
    
    formations = [
        {'name': '4-4-2', 'defenders': 4, 'midfielders': 4, 'forwards': 2},
        {'name': '4-3-3', 'defenders': 4, 'midfielders': 3, 'forwards': 3},
        {'name': '4-2-3-1', 'defenders': 4, 'midfielders': 5, 'forwards': 1},
        {'name': '5-3-2', 'defenders': 5, 'midfielders': 3, 'forwards': 2},
        {'name': '5-4-1', 'defenders': 5, 'midfielders': 4, 'forwards': 1},
        {'name': '3-2-4-1', 'defenders': 3, 'midfielders': 6, 'forwards': 1},
        {'name': '3-4-3', 'defenders': 3, 'midfielders': 4, 'forwards': 3},
    ]

    for data in formations:
        obj, created = Formation.objects.get_or_create(name=data['name'], defaults=data)
        estado = "✔️ Añadida" if created else "⚠️ Ya existía"
        print(f"{estado}: {data['name']}")

if __name__ == '__main__':
    run_seeder()
    print("\n✅ Tácticas listas para usarse.")