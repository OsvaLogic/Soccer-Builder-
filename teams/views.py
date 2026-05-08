# Archivo: teams/views.py
# Etiqueta: Vistas de la app Teams

from django.shortcuts import render
from .models import Team, Formation, Player

def pitch_view(request):
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
