# Archivo: teams/urls.py
# Etiqueta: Rutas de la app Teams

from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.pitch_view, name='pitch'),
    path('save-positions/', views.save_positions, name='save_positions'),
    path('edit-player/<int:player_id>/', views.edit_player, name='edit_player'),
]
