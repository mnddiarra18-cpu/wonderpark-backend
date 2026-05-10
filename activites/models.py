from django.db import models

class Activite(models.Model):
    TYPES = [
        ('piscine', 'Piscine'),
        ('aire_jeu', 'Aire de Jeu'),
    ]
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    type = models.CharField(max_length=20, choices=TYPES)
    capacite_max = models.IntegerField(default=50)
    statut = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

class Formule(models.Model):
    TYPES = [
        ('demi_journee', 'Demi-Journée'),
        ('journee_entiere', 'Journée Entière'),
        ('aire_jeu_1h', 'Aire de Jeu 1h'),
        ('aire_jeu_2h', 'Aire de Jeu 2h'),
        ('anniversaire', 'Anniversaire'),
    ]
    nom = models.CharField(max_length=100)
    type = models.CharField(max_length=20, choices=TYPES)
    description = models.TextField(blank=True)
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    duree = models.CharField(max_length=50)
    gouter_inclus = models.BooleanField(default=False)
    activites = models.ManyToManyField(Activite, blank=True)
    statut = models.BooleanField(default=True)

    def __str__(self):
        return self.nom

class Creneau(models.Model):
    activite = models.ForeignKey(
        Activite,
        on_delete=models.CASCADE,
        related_name='creneaux'
    )
    date = models.DateField()
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    capacite_disponible = models.IntegerField()
    statut = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.activite} - {self.date} {self.heure_debut}"