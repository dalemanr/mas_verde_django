from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='clientes'),
    path('registrarClientes/', views.registrarCliente, name='registrar_clientes'), 
    path('editarCliente/<id>', views.editarClientes, name='editar_cliente'),
    path('edicionCliente/<id>', views.edicionClientes, name='edicionClientes'),
    path('eliminarCliente/<id>', views.eliminarClientes, name='eliminar_cliente'), 
]
