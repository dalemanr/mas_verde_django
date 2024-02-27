from django.urls import path
from .views import *

urlpatterns = [
    path('signup/', RegistrationView.as_view(), name='signup'),
]