# Archivo: teams/urls.py
# Etiqueta: Rutas de la app Teams

from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.pitch_view, name='pitch'),
]
