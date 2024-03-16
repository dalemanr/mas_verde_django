from django.db import models
from clientes.models import Clientes


# Create your models here.

class Pqrs(models.Model):
    fecha = models.DateField(auto_now_add=True)
    asunto = models.CharField(max_length=255)
    detalle = models.CharField(max_length=100)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.CharField(max_length=200)

    
