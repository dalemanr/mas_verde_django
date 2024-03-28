from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='devoluciones'),
    path('registarDevolucion', registarDevolucion, name='registarDevolucion'),
]