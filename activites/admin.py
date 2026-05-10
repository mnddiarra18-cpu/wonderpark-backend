from django.contrib import admin
from .models import Activite, Formule, Creneau

@admin.register(Formule)
class FormuleAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type', 'prix', 'duree', 'statut']

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'type', 'capacite_max', 'statut']

@admin.register(Creneau)
class CreneauAdmin(admin.ModelAdmin):
    list_display = [
        'activite', 'date',
        'heure_debut', 'heure_fin', 'capacite_disponible'
    ]