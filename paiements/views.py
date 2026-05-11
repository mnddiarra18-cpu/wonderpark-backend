from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Paiement
from .serializers import PaiementSerializer, CreerPaiementSerializer
from reservations.models import Reservation
import uuid

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def creer_paiement(request):
    serializer = CreerPaiementSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data

        # Si caissier ou admin, chercher sans filtrer par client
        if request.user.role in ['caissier', 'admin', 'gestionnaire']:
            reservation = get_object_or_404(
                Reservation,
                id=data['reservation_id']
            )
        else:
            # Client normal : vérifier que c'est sa réservation
            reservation = get_object_or_404(
                Reservation,
                id=data['reservation_id'],
                client=request.user
            )

        # Vérifier si paiement existe déjà
        if hasattr(reservation, 'paiement'):
            return Response(
                {'error': 'Paiement déjà effectué'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Créer le paiement
        paiement = Paiement.objects.create(
            reservation=reservation,
            montant=reservation.montant_total,
            mode_paiement=data['mode_paiement'],
            methode_paiement=data['methode_paiement'],
            statut='effectue',
            reference=f"PAY-{uuid.uuid4().hex[:8].upper()}"
        )

        # Confirmer la réservation
        reservation.statut = 'confirmee'
        reservation.save()

        return Response({
            'message': 'Paiement effectué avec succès',
            'paiement': PaiementSerializer(paiement).data,
            'reference': paiement.reference
        }, status=status.HTTP_201_CREATED)

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mes_paiements(request):
    paiements = Paiement.objects.filter(
        reservation__client=request.user
    ).order_by('-date_paiement')
    serializer = PaiementSerializer(paiements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def tous_paiements(request):
    if request.user.role not in ['admin', 'comptable', 'caissier']:
        return Response(
            {'error': 'Accès non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )
    paiements = Paiement.objects.all().order_by('-date_paiement')
    serializer = PaiementSerializer(paiements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def statistiques_paiements(request):
    if request.user.role not in ['admin', 'comptable']:
        return Response(
            {'error': 'Accès non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )
    from django.db.models import Sum, Count
    stats = Paiement.objects.filter(
        statut='effectue'
    ).aggregate(
        total=Sum('montant'),
        nombre=Count('id')
    )
    return Response({
        'total': float(stats['total'] or 0),
        'nombre_transactions': stats['nombre'] or 0
    })

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def rembourser_paiement(request, pk):
    if request.user.role not in ['admin', 'comptable']:
        return Response(
            {'error': 'Accès non autorisé'},
            status=status.HTTP_403_FORBIDDEN
        )
    paiement = get_object_or_404(Paiement, pk=pk)
    paiement.statut = 'rembourse'
    paiement.save()
    paiement.reservation.statut = 'annulee'
    paiement.reservation.save()
    return Response({'message': 'Remboursement effectué'})