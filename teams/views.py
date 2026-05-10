# Archivo: teams/views.py
# Etiqueta: Vistas de la app Teams

from django.shortcuts import render
from .models import Team, Formation, Player

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
    team = None
    players = []
    
    if request.user.is_authenticated:
        team = Team.objects.filter(user=request.user).first()
        if team:
            players = team.players.all()
            
    formations = Formation.objects.all()

    context = {
        'team': team,
        'players': players,
        'formations': formations,
    }
    return render(request, 'teams/pitch.html', context)
