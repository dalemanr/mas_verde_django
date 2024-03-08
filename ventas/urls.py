from django.urls import path
from .views import *
from clientes.views import registrarCliente

urlpatterns = [
    path('', registrar_venta, name='venta'),
    path('clientes/', registrarCliente, name='registrarCliente'),
    path('recibo/<int:venta_id>/', recibo, name='recibo')
]