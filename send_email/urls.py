from django.urls import path
from . import views

from pqrs.views import registrarPqrs

urlpatterns = [
    path('', views.index, name='index'),
    path('email/<id>', views.correo, name='email'),
]


