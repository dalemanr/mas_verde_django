from django.forms import forms, ModelForm

from .models import *

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'total']