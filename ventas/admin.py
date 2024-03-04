from django.contrib import admin

from ventas.models import *

# Register your models here.

class DetalleVentaInline(admin.TabularInline):
    model = DetalleVenta
    extra = 1

class VentaAdmin(admin.ModelAdmin):
    inlines = [
        DetalleVentaInline,
    ]

admin.site.register(Venta, VentaAdmin)