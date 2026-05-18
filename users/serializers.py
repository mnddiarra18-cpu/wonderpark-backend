from rest_framework import serializers
from .models import Utilisateur
import re


class UtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = Utilisateur
        fields = [
            'id', 'username', 'first_name', 'last_name',
            'email', 'telephone', 'role', 'statut',
            'date_creation'
        ]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = Utilisateur
        fields = [
            'first_name', 'last_name', 'email',
            'telephone', 'password', 'confirm_password'
        ]

    def validate_email(self, value):
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, value):
            raise serializers.ValidationError("Format email invalide")
        if Utilisateur.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                "Un compte avec cet email existe déjà"
            )
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins 8 caractères"
            )
        if not re.search(r'[A-Z]', value):
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins une majuscule"
            )
        if not re.search(r'[0-9]', value):
            raise serializers.ValidationError(
                "Le mot de passe doit contenir au moins un chiffre"
            )
        return value

    def validate_telephone(self, value):
        pattern = r'^[0-9]{9,15}$'
        clean = value.replace(' ', '').replace('-', '')
        if not re.match(pattern, clean):
            raise serializers.ValidationError(
                "Numéro de téléphone invalide"
            )
        return value

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError(
                {"confirm_password": "Les mots de passe ne correspondent pas"}
            )
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        email = validated_data['email']
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