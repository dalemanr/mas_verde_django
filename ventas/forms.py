# forms.py
from django import forms
from .models import Venta, DetalleVenta

class VentaForm(forms.ModelForm):
    class Meta:
        model = Venta
        fields = ['cliente']

class DetalleVentaForm(forms.ModelForm):
    class Meta:
        model = DetalleVenta
        fields = ['producto', 'cantidad']



DetalleVentaFormSet = forms.inlineformset_factory(Venta, DetalleVenta, form=DetalleVentaForm, extra=1, exclude=['DELETE'])

