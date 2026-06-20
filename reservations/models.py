from django.db import models

class Reservation(models.Model):
    STATUTS = [
        ('en_attente', 'En attente'),
        ('confirmee', 'Confirmée'),
        ('annulee', 'Annulée'),
    ]
    MODES_PAIEMENT = [
        ('en_ligne', 'En ligne'),
        ('sur_place', 'Sur place'),
    ]

    client = models.ForeignKey(
        'users.Utilisateur',
        on_delete=models.CASCADE,
        related_name='reservations'
    )
    formule = models.ForeignKey(
        'activites.Formule',
        on_delete=models.SET_NULL,
        null=True
    )
    creneau = models.ForeignKey(
        'activites.Creneau',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    date_reservation = models.DateTimeField(auto_now_add=True)
    nombre_enfants = models.IntegerField(default=1)
    nombre_accompagnateurs = models.IntegerField(default=1)
    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='en_attente'
    )
    montant_total = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    notes = models.TextField(blank=True)
    
    mode_paiement_choisi = models.CharField(  
        max_length=20,
        choices=MODES_PAIEMENT,
        default='sur_place',
        blank=True
    )
    
def __str__(self):
        return f"Réservation {self.id}"


class Enfant(models.Model):
    reservation = models.ForeignKey(
        Reservation,
        on_delete=models.CASCADE,
        related_name='enfants'
    )
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"Enfant {self.age} ans"