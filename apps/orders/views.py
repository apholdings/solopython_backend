from rest_framework_api.views import StandardAPIView
from rest_framework import permissions


class CreateOrderView(StandardAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        data = request.data
        return self.send_response("payment")
