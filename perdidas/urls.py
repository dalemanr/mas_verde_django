from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='perdidas'),
    path('registroPerdida', registroPerdida, name='registroPerdida'),
]