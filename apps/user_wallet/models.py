import secrets, json, os
from djoser.signals import user_registered
from django.db import models

from django.conf import settings
import LWE4 as lwe

from eth_account import Account
from web3 import Web3

polygon_rpc = settings.POLYGON_RPC
ethereum_rpc = settings.ETHEREUM_RPC

User = settings.AUTH_USER_MODEL


class Wallet(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="user_wallet"
    )
    # Ethereum Wallet
    address = models.CharField(max_length=255)
    private_key = models.JSONField()


def create_user_wallet(request, user, *args, **kwargs):
    public_key_path = os.path.join(settings.BASE_DIR, "public_key.json")
    with open(public_key_path, "r") as f:
        public_key = json.load(f)

    # 1. Crear llaves Publica y Privada de Ethereum
    priv = secrets.token_hex(32)
    private_key = "0x" + priv
    acct = Account.from_key(private_key)

    # 2. Encriptar llave privada con algoritmo de latices
    encrypted_private_key = lwe.encrypt.encrypt(private_key, public_key)

    # 3. Crear wallet de usuario y guardar informacion
    Wallet.objects.create(
        user=user, private_key=encrypted_private_key, address=acct.address
    )


user_registered.connect(create_user_wallet)
