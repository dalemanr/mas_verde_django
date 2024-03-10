from django.urls import path
from .views import *
from clientes.views import registrarCliente

urlpatterns = [
    path('', registrar_venta, name='venta'),
    path('clientes/', registrarCliente, name='registrarCliente'),
    path('recibo/<int:venta_id>/', recibo, name='recibo'),
    path('lista_ventas', ventas_list, name='lista_ventas'),
    path('generar_pdf/<int:venta_id>/', generar_pdf, name='generar_pdf'),
]