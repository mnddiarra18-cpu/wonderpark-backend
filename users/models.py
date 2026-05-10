from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLES = [
        ('client', 'Client'),
        ('admin', 'Administrateur'),
        ('gestionnaire', 'Gestionnaire'),
        ('caissier', 'Caissier'),
        ('comptable', 'Comptable'),
    ]

    telephone = models.CharField(max_length=20, blank=True)
    role = models.CharField(
        max_length=20,
        choices=ROLES,
        default='client'
    )
    date_creation = models.DateTimeField(auto_now_add=True)
    statut = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.role})"