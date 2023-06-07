from django.urls import path
from .views import *

urlpatterns = [path("mercado_pago/", CreditCardPaymentView.as_view())]
