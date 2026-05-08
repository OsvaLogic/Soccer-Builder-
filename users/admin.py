# Archivo: users/admin.py
# Etiqueta: Configuración del panel de administración para Users

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)
