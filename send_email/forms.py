from django import forms

class FormularioContacto(forms.Form):
    
    asunto=forms.CharField(label='Asunto', required=True, max_length=30)
    contenido=forms.CharField(label='Contenido', max_length=400, widget=forms.Textarea )