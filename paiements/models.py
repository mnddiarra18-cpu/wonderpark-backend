from django.db import models

class Paiement(models.Model):
    MODES = [
        ('en_ligne', 'En ligne'),
        ('sur_place', 'Sur place'),
    ]
    METHODES = [
        ('carte', 'Carte Bancaire'),
        ('orange_money', 'Orange Money'),
        ('wave', 'Wave'),
        ('especes', 'Espèces'),
    ]
    STATUTS = [
        ('en_attente', 'En attente'),
        ('effectue', 'Effectué'),
        ('rembourse', 'Remboursé'),
    ]
    reservation = models.OneToOneField(
        'reservations.Reservation',
        on_delete=models.CASCADE,
        related_name='paiement'
    )
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    date_paiement = models.DateTimeField(auto_now_add=True)
    mode_paiement = models.CharField(max_length=20, choices=MODES)
    methode_paiement = models.CharField(
        max_length=20,
        choices=METHODES,
        blank=True
    )
    statut = models.CharField(
        max_length=20,
        choices=STATUTS,
        default='en_attente'
    )
    reference = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"Paiement {self.reference}"