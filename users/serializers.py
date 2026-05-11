from rest_framework import serializers
from .models import Utilisateur

class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telephone', 'role', 'statut',
            'date_creation'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            'first_name', 'last_name', 'email',
            'telephone', 'password', 'confirm_password'
        ]

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                "Les mots de passe ne correspondent pas"
            )
        return data
def create(self, validated_data):
    validated_data.pop('confirm_password')
    
    # Vérifier si l'email existe déjà
    email = validated_data['email']
    if Utilisateur.objects.filter(email=email).exists():
        raise serializers.ValidationError(
            {"email": "Un compte avec cet email existe déjà"}
        )
    
    user = Utilisateur.objects.create_user(
        username=email,
        email=email,
        first_name=validated_data['first_name'],
        last_name=validated_data['last_name'],
        telephone=validated_data.get('telephone', ''),
        password=validated_data['password'],
        role='client'
    )
    return user
    

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()