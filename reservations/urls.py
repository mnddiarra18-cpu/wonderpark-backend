from django.urls import path
from . import views

urlpatterns = [
    path('creer/', views.creer_reservation,
         name='creer_reservation'),
    path('mes-reservations/', views.mes_reservations,
         name='mes_reservations'),
    path('<int:pk>/', views.detail_reservation,
         name='detail_reservation'),
    path('<int:pk>/annuler/', views.annuler_reservation,
         name='annuler_reservation'),
    path('toutes/', views.toutes_reservations,
         name='toutes_reservations'),
    path('<int:pk>/statut/', views.modifier_statut_reservation,
         name='modifier_statut'),
]