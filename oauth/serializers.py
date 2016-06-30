from rest_framework import serializers

from oauth.constants import Scopes
from .models import Token, Grant, Application


# Social Auth


class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('access_token', 'refresh_token')


class AccessTokenSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=255, required=True)


class RefreshTokenSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=255, required=True)
    client_secret = serializers.CharField(max_length=255, required=True)
    refresh_token = serializers.CharField(max_length=255, required=True)


class GrantCodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grant
        fields = ('code',)


class ApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application


class ApplicationRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ('name', 'description', 'redirect_uri', 'site_uri')


class ApplicationAuthSerializer(serializers.Serializer):
    state = serializers.CharField(max_length=255, required=False)
    scope = serializers.CharField(max_length=32, default=Scopes.Read, required=False)
    redirect_uri = serializers.URLField(max_length=255, required=False)
    client_id = serializers.CharField(max_length=255, required=True)


class ApplicationAccessTokenSerializer(serializers.Serializer):
    client_id = serializers.CharField(max_length=255, required=True)
    client_secret = serializers.CharField(max_length=255, required=True)
    code = serializers.CharField(max_length=255, required=True)
    redirect_uri = serializers.URLField(max_length=255, required=False)
    state = serializers.CharField(max_length=255, required=False)
