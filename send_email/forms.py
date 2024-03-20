from django import forms
from django.forms import ModelForm

class FormularioContacto(forms.Form):
    
    asunto=forms.CharField(label='Asunto', required=True, max_length=30 )
    contenido=forms.CharField(label='Contenido', max_length=400, widget=forms.Textarea )