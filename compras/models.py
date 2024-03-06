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
    precio = models.IntegerField(null=True, blank=True, default=0)
    stock_disponible = models.IntegerField(default=0)
    fecha_creacion = models.DateField(auto_now_add=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to='productos/', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Compra(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.IntegerField(default=0)
    fecha_compra = models.DateField(auto_now_add=True)
    total = models.IntegerField(null=True, blank=True)
    precio_unitario = models.IntegerField(null=True, blank=True, default=0)
    porcentaje_ganancia = models.IntegerField(null=True, blank=True, default=0)

    def __str__(self):
        return f"Compra de {self.cantidad} unidades de {self.producto.nombre}"