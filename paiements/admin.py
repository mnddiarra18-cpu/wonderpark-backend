from django.contrib import admin
from .models import Paiement

@admin.register(Paiement)
class PaiementAdmin(admin.ModelAdmin):
    list_display = [
        'reference', 'montant',
        'methode_paiement', 'statut', 'date_paiement'
    ]
    list_filter = ['statut', 'methode_paiement']