from rest_framework import serializers
from .models import Reservation, Enfant
from activites.models import Formule

class EnfantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enfant
        fields = ['id', 'age']

class ReservationSerializer(serializers.ModelSerializer):
    enfants = EnfantSerializer(many=True, read_only=True)
    client_nom = serializers.SerializerMethodField()
    formule_nom = serializers.SerializerMethodField()
    mode_paiement = serializers.SerializerMethodField()
    methode_paiement = serializers.SerializerMethodField()
    class Meta:
        model = Reservation
        fields = [
            'id', 'client', 'client_nom', 'formule',
            'formule_nom', 'creneau', 'date_reservation',
            'nombre_enfants', 'nombre_accompagnateurs',
            'statut', 'montant_total', 'notes', 'enfants',
            'mode_paiement', 'methode_paiement'

        ]

    def get_client_nom(self, obj):
        return f"{obj.client.first_name} {obj.client.last_name}"

    def get_formule_nom(self, obj):
        return obj.formule.nom if obj.formule else None
    
    def get_methode_paiement(self, obj):
    try:
        paiement = obj.paiement
        return paiement.methode_paiement
    except Exception:
        return None

def get_mode_paiement(self, obj):
    try:
        return obj.mode_paiement
    except Exception:
        return None
class CreerReservationSerializer(serializers.Serializer):
    formule_id = serializers.IntegerField()
    date = serializers.DateField()
    nombre_enfants = serializers.IntegerField(min_value=1)
    nombre_accompagnateurs = serializers.IntegerField(min_value=0)
    enfants = EnfantSerializer(many=True, required=False, default=[])
    mode_paiement = serializers.ChoiceField(
        choices=['en_ligne', 'sur_place']
    )
    notes = serializers.CharField(required=False, allow_blank=True)
    genre_anniversaire = serializers.CharField(
        required=False, allow_blank=True
    )
    theme_anniversaire = serializers.CharField(
        required=False, allow_blank=True
    )
    age_anniversaire = serializers.CharField(
        required=False, allow_blank=True
    )
    notes = serializers.CharField(required=False, allow_blank=True)

    def validate_formule_id(self, value):
        try:
            Formule.objects.get(id=value)
        except Formule.DoesNotExist:
            raise serializers.ValidationError("Formule introuvable")
        return value