from django.urls import path
from .views import *

urlpatterns = [
    path('', registrar_venta, name='venta'),
    path('recibo/<int:venta_id>/', recibo, name='recibo')
]