from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from compras.models import *
from registration.views import group_required
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
# Create your views here.

####################Devoluciones#######################

@group_required("Administrador")
def index(request):
    devoluciones = Devolucion.objects.all()
    form = DevolucionForm()
    return render(request, "devoluciones/devoluciones.html", {"devoluciones": devoluciones, "form": form})

def registarDevolucion(request):
    if request.method == 'POST':
        producto = (request.POST["producto"])
        cliente = (request.POST["cliente"])
        cantidad = int(request.POST["cantidad"])
        causa = (request.POST["causa"])

        devolucion = Devolucion(producto_id=producto, cantidad=cantidad, causa=causa, cliente_id=cliente)
        producto = devolucion.producto
        producto.stock_disponible += cantidad
        producto.save()
        devolucion.save()
        return redirect('devoluciones')
