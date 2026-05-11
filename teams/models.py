# Archivo: teams/models.py
# Etiqueta: Modelos de la app Teams

from django.db import models
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
    
    # Atributos estilo FC25
    pace = models.IntegerField(default=70)
    shooting = models.IntegerField(default=70)
    passing = models.IntegerField(default=70)
    dribbling = models.IntegerField(default=70)
    defending = models.IntegerField(default=70)
    physical = models.IntegerField(default=70)
    
    # Físico y Datos extra
    age = models.IntegerField(default=21)
    height = models.FloatField(default=1.80)
    weight = models.IntegerField(default=75)
    preferred_foot = models.CharField(max_length=20, default='Diestro')

    photo = models.ImageField(upload_to='players/', blank=True, null=True, default='default_player.png')
    
    pitch_x = models.FloatField(default=0.0)
    pitch_y = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-calcular el GRL (Rating) como promedio de las 6 estadísticas
        if getattr(self, 'position', 'MID') != 'GK':
            stats = [self.pace, self.shooting, self.passing, self.dribbling, self.defending, self.physical]
            self.rating = sum(stats) // 6
        super().save(*args, **kwargs)
