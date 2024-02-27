from django.forms import ModelForm

from compras.models import *

class CompraForm(ModelForm):
    class Meta:
        model = Compra
        fields = ['producto', 'cantidad', 'total']