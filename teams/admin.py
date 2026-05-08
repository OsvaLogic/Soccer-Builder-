# Archivo: teams/admin.py
# Etiqueta: Configuración del panel de administración para Teams

from django.contrib import admin
from .models import Formation, Team, Player

admin.site.register(Formation)
admin.site.register(Team)
admin.site.register(Player)
