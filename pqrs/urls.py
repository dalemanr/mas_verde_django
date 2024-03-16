from django.urls import path, include
from . import views



urlpatterns = [
    path('', views.index, name='pqrs'),
    path('listado_pqrs', views.listar_pqrs, name='listar_pqrs'),
    path('registrarPqrs', views.registrarPqrs, name='registrar_pqrs'),
    path('eliminarPqrs/<id>', views. eliminarPqrs, name='eliminar_pqrs'), 
]



