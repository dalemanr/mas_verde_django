from django.db import models

from compras.models import Producto


# Create your models here.
class Perdida(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha_perdida = models.DateField(auto_now_add=True)
    causa = models.TextField()

    def __str__(self):
        return f"perdida de {self.producto} con una cantidad de {self.cantidad} a causa de {self.causa}"