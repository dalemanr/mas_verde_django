from django import forms
from django.forms import ModelForm

from perdidas.models import Perdida


class PerdidaForm(ModelForm):
    class Meta:
        model = Perdida
        fields = ['producto', 'cantidad', 'causa']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'causa': forms.TextInput(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'})
        }