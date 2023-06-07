from rest_framework_api.views import StandardAPIView
from rest_framework import permissions
from .models import Wallet
from rest_framework import status
from .serializers import UserWalletSerializer


# Create your views here.
class MyUserWalletView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.send_response(
            UserWalletSerializer(Wallet.objects.get(user=self.request.user)).data,
            status=status.HTTP_200_OK,
        )
