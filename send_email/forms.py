from django import forms
from django.forms import ModelForm

from django import forms

class FormularioContacto(forms.Form):
    asunto = forms.CharField(label='Asunto', required=True, max_length=30, widget=forms.TextInput(attrs={'class': 'form-control'}))
    contenido = forms.CharField(label='Contenido', max_length=400, widget=forms.Textarea(attrs={'class': 'form-control'}))
