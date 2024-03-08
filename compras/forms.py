from django import forms
from django.forms import ModelForm

from compras.models import *

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'total', 'porcentaje_ganancia']
        widgets = {
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'total': forms.NumberInput(attrs={'class': 'form-control'}),
            'porcentaje_ganancia': forms.NumberInput(attrs={'class': 'form-control'}),
            'producto': forms.Select(attrs={'class': 'form-control'})
        }

class ImagenForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['imagen']