from django.contrib import admin
from .models import Reservation, Enfant

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'client', 'formule',
        'date_reservation', 'statut', 'montant_total'
    ]
    list_filter = ['statut']

@admin.register(Enfant)
class EnfantAdmin(admin.ModelAdmin):
    list_display = [ 'age', 'reservation']