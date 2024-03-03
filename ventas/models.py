from django.db import models

from compras.models import Producto


# Create your models here.

class Venta(models.Model):
    cliente = models.TextField(max_length=200)#llave del cliente
    producto = models.ManyToManyField(Producto)
    cantidad = models.IntegerField()
    fecha = models.DateField()
    vendedor = models.TextField(max_length=200)#llave del vendedor
    Total = models
