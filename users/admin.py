from django.contrib import admin
from .models import Utilisateur

@admin.register(Utilisateur)
class UtilisateurAdmin(admin.ModelAdmin):
    list_display = [
        'username', 'first_name', 'last_name',
        'email', 'role', 'statut'
    ]
    list_filter = ['role', 'statut']