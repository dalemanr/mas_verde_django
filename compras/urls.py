from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='compras'),
    path('registrarCompra', registrarCompra, name='registrarCompra'),
    path('detalleCompra/<int:id>', verDetalleCompra, name='detalleCompra'),
    path('detalleCompra/<int:id>/eliminarCompra', eliminarCompra, name='eliminarCompra'),
    path('reporteCompras', compras_por_proveedor, name='reporteCompras'),
]