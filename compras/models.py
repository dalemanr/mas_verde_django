from django.db import models

# Create your models here.
class Proveedor(models.Model):
    nombre = models.CharField(max_length=250)
    nit = models.CharField(max_length=250)
    telefono = models.CharField(max_length=12)
    correo = models.EmailField(max_length=100)

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255)
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    stock_disponible = models.IntegerField()
    fecha_creacion = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    fecha_compra = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self):
        return f"Compra de {self.cantidad} unidades de {self.producto.nombre}"