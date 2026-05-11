# Archivo: teams/views.py
# Etiqueta: Vistas de la app Teams

import json
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from .models import Team, Formation, Player

User = get_user_model()

def home_view(request):
    """Vista del Menú Principal"""
    return render(request, 'teams/home.html')

def dashboard_view(request):
    """Vista estilo FIFA para ver todas las plantillas"""
    teams = []
    if request.user.is_authenticated:
        teams = Team.objects.filter(user=request.user)
    return render(request, 'teams/dashboard.html', {'teams': teams})

def pitch_view(request):
    """Vista de la Pizarra Interactiva"""
    if request.user.is_authenticated:
        user = request.user
    else:
        # Auto-crear un usuario demo para que funcione sin necesidad de login
        user, created = User.objects.get_or_create(username="demo_user", defaults={"email": "demo@demo.com"})

    # Obtener o crear un equipo por defecto
    team, team_created = Team.objects.get_or_create(user=user, defaults={"name": "Equipo Ideal FC"})

    default_positions = ['GK', 'DEF', 'DEF', 'DEF', 'DEF', 'MID', 'MID', 'MID', 'MID', 'FWD', 'FWD']
    default_coords = [
        (50, 90), (20, 75), (40, 80), (60, 80), (80, 75),
        (20, 50), (40, 50), (60, 50), (80, 50), (40, 20), (60, 20)
    ]

    # Auto-generar 11 jugadores genéricos si el equipo está vacío
    current_players = team.players.count()
    if current_players < 11:
        for i in range(current_players, 11):
            Player.objects.create(
                team=team,
                name=f"Jugador Genérico {i+1}",
                position=default_positions[i] if i < 11 else 'MID',
                rating=75,
                pitch_x=default_coords[i][0] if i < 11 else 50,
                pitch_y=default_coords[i][1] if i < 11 else 50
            )
            
    players = list(team.players.all())
            
    # Reparar jugadores que quedaron apilados en la esquina (0, 0) por registros antiguos
    for i, player in enumerate(players):
        if player.pitch_x == 0.0 and player.pitch_y == 0.0 and i < 11:
            player.pitch_x = default_coords[i][0]
            player.pitch_y = default_coords[i][1]
            player.save()
            
        # Prevenir que Django ponga comas en los decimales y rompa el CSS
        player.safe_x = str(float(player.pitch_x)).replace(',', '.')
        player.safe_y = str(float(player.pitch_y)).replace(',', '.')

    formations = Formation.objects.all()

    context = {
        'team': team,
        'players': players,
        'formations': formations,
    }
    return render(request, 'teams/pitch.html', context)

def save_positions(request):
    """Guarda las posiciones y estadísticas de los jugadores en la base de datos"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            for p_data in data.get('players', []):
                player = Player.objects.filter(id=p_data['id']).first()
                if player:
                    # Actualizar posiciones
                    player.pitch_x = p_data.get('x', player.pitch_x)
                    player.pitch_y = p_data.get('y', player.pitch_y)
                    
                    # Actualizar atributos si están presentes
                    if 'name' in p_data: player.name = p_data['name']
                    if 'pace' in p_data: player.pace = int(p_data['pace'])
                    if 'shooting' in p_data: player.shooting = int(p_data['shooting'])
                    if 'passing' in p_data: player.passing = int(p_data['passing'])
                    if 'dribbling' in p_data: player.dribbling = int(p_data['dribbling'])
                    if 'defending' in p_data: player.defending = int(p_data['defending'])
                    if 'physical' in p_data: player.physical = int(p_data['physical'])
                    if 'age' in p_data: player.age = int(p_data['age'])
                    if 'height' in p_data: player.height = float(p_data['height'])
                    if 'weight' in p_data: player.weight = int(p_data['weight'])
                    if 'foot' in p_data: player.preferred_foot = p_data['foot']
                    
                    player.save() # El GRL se recalculará automáticamente aquí
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid method'})

def edit_player(request, player_id):
    """Actualiza la información de un jugador individual, incluyendo su foto"""
    if request.method == 'POST':
        try:
            player = Player.objects.get(id=player_id)
            
            # Actualizar campos básicos
            player.name = request.POST.get('name', player.name)
            player.age = int(request.POST.get('age', player.age) or 21)
            player.height = float(request.POST.get('height', player.height) or 1.80)
            player.weight = int(request.POST.get('weight', player.weight) or 75)
            player.preferred_foot = request.POST.get('foot', player.preferred_foot)
            
            # Actualizar stats
            player.pace = int(request.POST.get('pace', player.pace) or 70)
            player.shooting = int(request.POST.get('shooting', player.shooting) or 70)
            player.passing = int(request.POST.get('passing', player.passing) or 70)
            player.dribbling = int(request.POST.get('dribbling', player.dribbling) or 70)
            player.defending = int(request.POST.get('defending', player.defending) or 70)
            player.physical = int(request.POST.get('physical', player.physical) or 70)
            
            # Actualizar foto si se subió una
            if 'photo' in request.FILES:
                player.photo = request.FILES['photo']
                
            player.save() # Calcula automáticamente el GRL
            return JsonResponse({'status': 'success', 'photo_url': player.photo.url if player.photo else '', 'rating': player.rating})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    return JsonResponse({'status': 'invalid method'})
