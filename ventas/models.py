from django.contrib.auth import get_user# este es el metodo para obtener el usuario que inicio sesion
from django.db import models
from clientes.models import Clientes
from compras.models import Producto
from registration.models import User


# Create your models here.

class Venta(models.Model):
    fecha = models.DateField(auto_now_add=True)
    productos = models.ManyToManyField(Producto, through='DetalleVenta')
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE, null=True, blank=True)
    vendedor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    total = models.DecimalField(max_digits=30, decimal_places=2)

    def set_vendedor(self):
        self.vendedor = get_user # en realidad esto va en una vista a la hora de crear la venta pero lo ponemos aca para no perderlo xd y no es una funcion

    def __str__(self):
        return f"venta del cliente {self.cliente}"
class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=30, decimal_places=2)
    def __str__(self):
        return f"{self.producto} - Cantidad: {self.cantidad}"
