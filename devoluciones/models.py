from django.db import models

from compras.models import Producto
from clientes.models import Clientes

# Create your models here.
class Devolucion(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True, blank=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha_devolucion = models.DateField(auto_now_add=True)
    causa = models.TextField()

    def __str__(self):
        return f"devolucion de {self.producto} co una cantidad de {self.cantidad}"