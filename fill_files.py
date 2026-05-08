import os

file_contents = {
    ".env": """DEBUG=True
SECRET_KEY=django-insecure-tu-clave-secreta-aqui
DATABASE_URL=postgres://tu_usuario:tu_contraseña@localhost:5432/soccer_db
""",

    "requirements.txt": """Django>=4.2,<5.0
psycopg2-binary>=2.9.9
django-environ>=0.11.2
Pillow>=10.0.0
django-allauth>=0.58.2
requests>=2.0.0
""",

    "core/settings.py": """import os
from pathlib import Path
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

SECRET_KEY = env('SECRET_KEY', default='unsafe-secret-key')
DEBUG = env.bool('DEBUG', default=True)
ALLOWED_HOSTS = ['*']

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users',
    'teams',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

DATABASES = {
    'default': env.db('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

LANGUAGE_CODE = 'es-es'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

AUTH_USER_MODEL = 'users.CustomUser'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Redirecciones después de iniciar o cerrar sesión
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
""",

    "core/urls.py": """from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('', include('teams.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
""",

    "users/models.py": """from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    def __str__(self):
        return self.username
""",

    "users/admin.py": """from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

admin.site.register(CustomUser, UserAdmin)
""",

    "users/urls.py": """from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
]
""",

    "teams/models.py": """from django.db import models
from django.conf import settings

class Formation(models.Model):
    name = models.CharField(max_length=10, unique=True)
    defenders = models.IntegerField(default=4)
    midfielders = models.IntegerField(default=4)
    forwards = models.IntegerField(default=2)

    def __str__(self):
        return self.name

class Team(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=100)
    formation = models.ForeignKey(Formation, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.user.username})"

class Player(models.Model):
    POSITION_CHOICES = [
        ('GK', 'Goalkeeper'),
        ('DEF', 'Defender'),
        ('MID', 'Midfielder'),
        ('FWD', 'Forward'),
    ]

    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name = models.CharField(max_length=100)
    position = models.CharField(max_length=3, choices=POSITION_CHOICES)
    rating = models.IntegerField(default=75)
    
    nationality = models.CharField(max_length=50, blank=True, null=True)
    club = models.CharField(max_length=100, blank=True, null=True)
    
    photo = models.ImageField(upload_to='players/', blank=True, null=True, default='default_player.png')
    
    pitch_x = models.FloatField(default=0.0)
    pitch_y = models.FloatField(default=0.0)

    def __str__(self):
        return self.name
""",

    "teams/admin.py": """from django.contrib import admin
from .models import Formation, Team, Player

admin.site.register(Formation)
admin.site.register(Team)
admin.site.register(Player)
""",

    "teams/views.py": """from django.shortcuts import render
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
""",

    "teams/urls.py": """from django.urls import path
from . import views

app_name = 'teams'

urlpatterns = [
    path('', views.pitch_view, name='pitch'),
]
""",

    "templates/base.html": """{% load static %}
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Soccer Team Builder</title>
    <link rel="stylesheet" href="{% static 'css/style.css' %}">
    <link rel="stylesheet" href="{% static 'css/pitch.css' %}">
</head>
<body>
    <nav class="navbar">
        <div class="logo">⚽ Soccer Builder</div>
        <ul class="nav-links">
            <li><a href="{% url 'teams:pitch' %}">Mi Pizarra</a></li>
            {% if user.is_authenticated %}
                <li><a href="#">Mis Plantillas</a></li>
                <li><a href="#">Hola, {{ user.username }}</a></li>
            {% else %}
                <li><a href="#">Iniciar Sesión</a></li>
            {% endif %}
        </ul>
    </nav>

    <main class="container">
        {% block content %}
        {% endblock %}
    </main>

    <script src="{% static 'js/main.js' %}"></script>
    {% block extra_js %}{% endblock %}
</body>
</html>
""",

    "templates/teams/pitch.html": """{% extends 'base.html' %}
{% load static %}

{% block content %}
<div class="pitch-container">
    <div class="toolbar">
        <h2>Mi Pizarra Interactiva</h2>
        <select id="formation-select">
            <option value="">Selecciona Formación</option>
            {% for form in formations %}
                <option value="{{ form.name }}">{{ form.name }}</option>
            {% endfor %}
        </select>
        <button id="save-team-btn" class="btn">Guardar Plantilla</button>
    </div>

    <div class="soccer-pitch" id="pitch">
        {% if players %}
            {% for player in players %}
                <div class="player-card" style="left: {{ player.pitch_x }}%; top: {{ player.pitch_y }}%;">
                    <img src="{{ player.photo.url }}" alt="{{ player.name }}" class="player-photo">
                    <div class="player-info">
                        <span class="player-name">{{ player.name }}</span>
                        <span class="player-rating">{{ player.rating }}</span>
                    </div>
                </div>
            {% endfor %}
        {% else %}
            <p class="empty-pitch-msg">Agrega jugadores desde el menú lateral para comenzar.</p>
        {% endif %}
    </div>

    <!-- Incluir el modal de edición de jugadores -->
    {% include 'teams/player_modal.html' %}
</div>
{% endblock %}

{% block extra_js %}
<script src="{% static 'js/pitch.js' %}"></script>
<script src="{% static 'js/drag_drop.js' %}"></script>
{% endblock %}
""",

    "static/css/style.css": """:root {
    --primary-color: #2e7d32;
    --bg-color: #f4f4f9;
    --text-color: #333;
}

* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

body {
    background-color: var(--bg-color);
    color: var(--text-color);
}

.navbar {
    background-color: var(--primary-color);
    color: white;
    display: flex;
    justify-content: space-between;
    padding: 1rem 2rem;
    align-items: center;
}

.nav-links {
    list-style: none;
    display: flex;
    gap: 1.5rem;
}

.nav-links a {
    color: white;
    text-decoration: none;
    font-weight: bold;
}

.container {
    padding: 2rem;
    max-width: 1200px;
    margin: 0 auto;
}

.btn {
    background-color: #1565c0;
    color: white;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

/* --- Estilos para el Modal --- */
.modal {
    display: none;
    position: fixed;
    z-index: 2000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0, 0, 0, 0.5);
    justify-content: center;
    align-items: center;
}

.modal-content {
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    width: 300px;
    text-align: center;
    position: relative;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
}

.close-modal {
    position: absolute;
    top: 10px;
    right: 15px;
    font-size: 1.5rem;
    font-weight: bold;
    cursor: pointer;
    color: #333;
}

.form-control {
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
    width: 100%;
}
""",

    "static/css/pitch.css": """.pitch-container {
    display: flex;
    flex-direction: column;
    gap: 1rem;
}

.toolbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: white;
    padding: 1rem;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.soccer-pitch {
    position: relative;
    width: 100%;
    height: 600px;
    background-color: #4caf50;
    background-image: linear-gradient(rgba(255, 255, 255, 0.3) 1px, transparent 1px),
                      linear-gradient(90deg, rgba(255, 255, 255, 0.3) 1px, transparent 1px);
    background-size: 50px 50px;
    border: 3px solid white;
    border-radius: 10px;
    margin: 0 auto;
    overflow: hidden;
}

.player-card {
    position: absolute;
    width: 80px;
    background: white;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    text-align: center;
    padding: 5px;
    cursor: grab;
    transform: translate(-50%, -50%);
}

.player-photo {
    width: 50px;
    height: 50px;
    border-radius: 50%;
    object-fit: cover;
}

.player-info {
    display: flex;
    flex-direction: column;
    font-size: 0.8rem;
    margin-top: 5px;
}

.player-rating {
    font-weight: bold;
    color: #d32f2f;
}
""",

    "manage.py": """#!/usr/bin/env python
import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("No se pudo importar Django.") from exc
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
""",

    "core/asgi.py": """import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_asgi_application()
""",

    "core/wsgi.py": """import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()
""",

    "users/apps.py": """from django.apps import AppConfig

class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
""",

    "teams/apps.py": """from django.apps import AppConfig

class TeamsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'teams'
""",

    "users/views.py": """from django.shortcuts import render

# Aquí irán las vistas del perfil de usuario
""",

    "static/js/drag_drop.js": """document.addEventListener('DOMContentLoaded', () => {
    const players = document.querySelectorAll('.player-card');
    const pitch = document.getElementById('pitch');

    let isDragging = false;
    let currentDragged = null;
    let offsetX = 0;
    let offsetY = 0;

    players.forEach(player => {
        player.addEventListener('mousedown', (e) => {
            isDragging = true;
            currentDragged = player;
            
            const rect = player.getBoundingClientRect();
            offsetX = e.clientX - rect.left;
            offsetY = e.clientY - rect.top;
            
            player.style.cursor = 'grabbing';
            player.style.zIndex = 1000;
        });
    });

    document.addEventListener('mousemove', (e) => {
        if (!isDragging || !currentDragged) return;

        const pitchRect = pitch.getBoundingClientRect();
        
        let newX = e.clientX - pitchRect.left - offsetX + (currentDragged.offsetWidth / 2);
        let newY = e.clientY - pitchRect.top - offsetY + (currentDragged.offsetHeight / 2);
        
        if (newX < 0) newX = 0;
        if (newY < 0) newY = 0;
        if (newX > pitchRect.width) newX = pitchRect.width;
        if (newY > pitchRect.height) newY = pitchRect.height;
        
        const xPercent = (newX / pitchRect.width) * 100;
        const yPercent = (newY / pitchRect.height) * 100;

        currentDragged.style.left = `${xPercent}%`;
        currentDragged.style.top = `${yPercent}%`;
    });

    document.addEventListener('mouseup', () => {
        if (currentDragged) {
            currentDragged.style.cursor = 'grab';
            currentDragged.style.zIndex = '';
        }
        isDragging = false;
        currentDragged = null;
    });
});
""",

    "static/js/pitch.js": """document.addEventListener('DOMContentLoaded', () => {
    const formationSelect = document.getElementById('formation-select');
    const saveBtn = document.getElementById('save-team-btn');

    if (formationSelect) {
        formationSelect.addEventListener('change', (e) => {
            const formation = e.target.value;
            if (formation) {
                console.log(`Cambiando a formación: ${formation}`);
            }
        });
    }

    if (saveBtn) {
        saveBtn.addEventListener('click', () => {
            alert("Posiciones registradas. (La petición al servidor se implementará pronto)");
        });
    }

    // --- Lógica del Modal ---
    const modal = document.getElementById('playerModal');
    const closeModalBtn = document.querySelector('.close-modal');
    const players = document.querySelectorAll('.player-card');

    players.forEach(player => {
        player.addEventListener('dblclick', (e) => {
            const playerName = player.querySelector('.player-name').innerText;
            const playerRating = player.querySelector('.player-rating').innerText;
            
            document.getElementById('playerNameInput').value = playerName;
            document.getElementById('playerRatingInput').value = playerRating;
            
            modal.style.display = 'flex';
        });
    });

    if (closeModalBtn) {
        closeModalBtn.addEventListener('click', () => modal.style.display = 'none');
    }

    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });
});
""",

    "static/js/main.js": """document.addEventListener('DOMContentLoaded', () => {
    console.log('Soccer Builder App iniciada correctamente.');
});
""",

    "static/js/external_api.js": """async function searchExternalPlayer(playerName) {
    console.log(`Buscando estadísticas de ${playerName}...`);
}
""",

    "templates/users/login.html": """{% extends 'base.html' %}
{% load socialaccount %}
{% block content %}
<div class="login-container" style="text-align: center; margin-top: 100px;">
    <h2>Inicia Sesión en Soccer Builder</h2>
    <a href="{% provider_login_url 'google' %}" class="btn" style="background-color: #db4437; padding: 15px 30px;">Entrar con Google</a>
</div>
{% endblock %}
""",

    "templates/teams/dashboard.html": """{% extends 'base.html' %}
{% block content %}
<div class="dashboard-container">
    <h2>Mis Plantillas Guardadas</h2>
    <a href="{% url 'teams:pitch' %}" class="btn" style="display: inline-block; margin-top: 15px;">Ir a la Pizarra</a>
</div>
{% endblock %}
""",

    "templates/teams/player_modal.html": """<div id="playerModal" class="modal" style="display: none;">
    <div class="modal-content">
        <span class="close-modal">&times;</span>
        <h2>Editar Jugador</h2>
        <form id="editPlayerForm" style="display: flex; flex-direction: column; gap: 10px; margin-top: 15px;">
            <input type="text" id="playerNameInput" placeholder="Nombre" class="form-control">
            <input type="number" id="playerRatingInput" placeholder="Valoración (ej. 85)" class="form-control">
            <button type="submit" class="btn">Guardar Cambios</button>
        </form>
    </div>
</div>
"""
}

for file_path, content in file_contents.items():
    # Normalizamos la ruta para evitar problemas entre Windows y los slashes '/'
    safe_path = os.path.normpath(file_path)
    if os.path.exists(safe_path):
        with open(safe_path, 'w', encoding='utf-8') as f:
            f.write(content)
            print(f"✔️ Rellenado exitosamente: {safe_path}")
    else:
        print(f"❌ El archivo {safe_path} no se encontró en la ubicación esperada.")
        
print("\\n¡Listo! Todos los archivos base han sido poblados.")