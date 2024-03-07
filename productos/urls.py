from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='productos'),
    path('registrarProducto/', views.registrarProducto, name='registrar_producto'),
    path('editarProducto/<id>', views.editarProducto, name='editar_producto'),
    path('edicionProducto/<id>', views.edicionProducto, name='edicionProductos'),
    path('eliminarProducto/<id>', views.eliminarProducto, name='eliminar_producto'),
]
