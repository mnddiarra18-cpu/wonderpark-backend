from rest_framework import serializers
from .models import Paiement

class PaiementSerializer(serializers.ModelSerializer):
    reservation_id = serializers.SerializerMethodField()
    client_nom = serializers.SerializerMethodField()

    class Meta:
        model = Paiement
        fields = [
            'id', 'reservation_id', 'client_nom',
            'montant', 'date_paiement', 'mode_paiement',
            'methode_paiement', 'statut', 'reference'
        ]

    def get_reservation_id(self, obj):
        return obj.reservation.id

    def get_client_nom(self, obj):
        client = obj.reservation.client
        return f"{client.first_name} {client.last_name}"

class CreerPaiementSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    methode_paiement = serializers.ChoiceField(
        choices=['carte', 'orange_money', 'wave', 'especes']
    )
    mode_paiement = serializers.ChoiceField(
        choices=['en_ligne', 'sur_place']
    )
    numero_mobile = serializers.CharField(
        required=False,
        allow_blank=True
    )