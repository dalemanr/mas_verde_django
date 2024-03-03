from django.contrib.auth import logout
from django.contrib.auth.decorators import user_passes_test

from .forms import *
from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django import forms

# Create your views here.

def group_required(*group_names):
    def in_groups(user):
        if user.groups.filter(name__in=group_names).exists():
            return True
        return False
    return user_passes_test(in_groups)

class RegistrationView(CreateView):
    form_class = UserCreationFormWithEmail
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(RegistrationView, self).get_form()
        form.fields['username'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Usuario'})
        form.fields['documento'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'documento'})
        form.fields['first_name'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Nombre'})
        form.fields['last_name'].widget = forms.TextInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Apellido'})
        form.fields['email'].widget = forms.EmailInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Email'})
        form.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Contraseña'})
        form.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control mb-2', 'placeholder': 'Repite la contraseñá'})


        return form

def salir(request):
    logout(request)
    return render(request, 'login')

