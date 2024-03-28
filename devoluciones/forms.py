from django import forms
from django.forms import ModelForm

from .models import *

class DevolucionForm(ModelForm):
    class Meta:
        model = Devolucion
        fields = ['producto', 'cantidad', 'causa']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'causa': forms.TextInput(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'})
        }
