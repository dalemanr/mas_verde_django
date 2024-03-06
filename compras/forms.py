from django.forms import ModelForm

from compras.models import *

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'total', 'porcentaje_ganancia']

class ImagenForm(ModelForm):
    class Meta:
        model = Producto
        fields = ['imagen']