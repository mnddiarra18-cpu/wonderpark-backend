from django.urls import path
from . import views

urlpatterns = [
    path('creer/', views.creer_paiement, name='creer_paiement'),
    path('mes-paiements/', views.mes_paiements, name='mes_paiements'),
    path('tous/', views.tous_paiements, name='tous_paiements'),
    path('statistiques/', views.statistiques_paiements,
         name='statistiques_paiements'),
    path('<int:pk>/rembourser/', views.rembourser_paiement,
         name='rembourser_paiement'),
         path('initier-wave/', views.initier_paiement_wave,
     name='initier_wave'),
]