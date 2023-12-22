from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator
from django.http import JsonResponse
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Добавьте дополнительные поля в токен
        token["email"] = user.email
        token["staff"] = user.is_staff

        return token


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
            # "login",
        ]

    # def validate(self, data):
    #     if User.objects.filter(email=data["email"]).exists():
    #         return Response(
    #             {"message": "Nickname already exists"},
    #             code=409,
    #         )
    #     if User.objects.filter(email=data["username"]).exists():
    #         return Response(
    #             {"message": "Nickname already exists"},
    #             code=409,
    #         )

    #     return data

    def create(self, validated_data):
        password = validated_data["password"]
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
