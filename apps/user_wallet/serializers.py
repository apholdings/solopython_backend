from rest_framework import serializers
from .models import *

class UserWalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'id',
            'user',
            'address',
        ]

class UserWalletPrivateKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = [
            'id',
            'user',
            'address',
            'private_key',
        ]
