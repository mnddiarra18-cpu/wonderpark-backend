from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Reservation, Enfant
from .serializers import ReservationSerializer, CreerReservationSerializer
from activites.models import Formule

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creer_reservation(request):
    if request.user.role not in ['client', 'admin']:
        return Response(
            {'error': 'Seuls les clients peuvent faire des réservations'},
            status=status.HTTP_403_FORBIDDEN
        )
    serializer = CreerReservationSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data

          # Vérifier que le nombre d'enfants est raisonnable
        if data['nombre_enfants'] > 20:
            return Response(
                {'error': 'Nombre d\'enfants maximum : 20'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Vérifier que la date n'est pas dans le passé
        from datetime import date
        if data.get('date') and data['date'] < date.today():
            return Response(
                {'error': 'La date de réservation ne peut pas être dans le passé'},
                status=status.HTTP_400_BAD_REQUEST
            )
        formule = get_object_or_404(Formule, id=data['formule_id'])

        # Calcul du montant
        prix_formule = formule.prix * data['nombre_enfants']
        accompagnateurs_pay = max(
            0, data['nombre_accompagnateurs'] - 1
        )
        prix_accompagnateurs = accompagnateurs_pay * 2000
        montant_total = prix_formule + prix_accompagnateurs

        # Créer la réservation
        reservation = Reservation.objects.create(
            client=request.user,
            formule=formule,
            nombre_enfants=data['nombre_enfants'],
            nombre_accompagnateurs=data['nombre_accompagnateurs'],
            montant_total=montant_total,
            notes=data.get('notes', ''),
            mode_paiement_choisi=data.get('mode_paiement', 'sur_place'),
            statut='en_attente'
        )

        # Créer les enfants seulement si présents
        enfants_data = data.get('enfants', [])
        for enfant_data in enfants_data:
            if enfant_data.get('age'):
                Enfant.objects.create(
                    reservation=reservation,
                    age=enfant_data['age']
                )

        return Response({
            'message': 'Réservation créée avec succès',
            'reservation': ReservationSerializer(reservation).data,
            'montant_total': float(montant_total)
        }, status=status.HTTP_201_CREATED)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_reservations(request):
    reservations = Reservation.objects.filter(
        client=request.user
    ).order_by('-date_reservation')
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def detail_reservation(request, pk):
    reservation = get_object_or_404(
        Reservation, pk=pk, client=request.user
    )
    serializer = ReservationSerializer(reservation)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def annuler_reservation(request, pk):
    reservation = get_object_or_404(
        Reservation, pk=pk, client=request.user
    )
    if reservation.statut == 'confirmee':
        return Response(
            {'error': 'Impossible d\'annuler une réservation confirmée'},
            status=status.HTTP_400_BAD_REQUEST
        )
    reservation.statut = 'annulee'
    reservation.save()
    return Response({'message': 'Réservation annulée avec succès'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def toutes_reservations(request):
    if request.user.role not in ['admin', 'gestionnaire', 'caissier']:
        return Response(
            {'error': 'Accès non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )
    reservations = Reservation.objects.all().order_by(
        '-date_reservation'
    )
    serializer = ReservationSerializer(reservations, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def modifier_statut_reservation(request, pk):
    if request.user.role not in ['admin', 'gestionnaire', 'caissier']:
        return Response(
            {'error': 'Accès non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )
    reservation = get_object_or_404(Reservation, pk=pk)
    nouveau_statut = request.data.get('statut')
    if nouveau_statut not in ['en_attente', 'confirmee', 'annulee']:
        return Response(
            {'error': 'Statut invalide'},
            status=status.HTTP_400_BAD_REQUEST
        )
    reservation.statut = nouveau_statut
    reservation.save()
    return Response({
        'message': 'Statut mis à jour',
        'reservation': ReservationSerializer(reservation).data
    })