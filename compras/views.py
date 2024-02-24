from django.shortcuts import render, redirect, get_object_or_404

from .forms import CompraForm
from .models import *
# Create your views here.

####################CRUD PRODUCTOS#######################












####################CRUD PROVEEDORES######################
















########################CRUD COMPRAS##########################

def index(request):
    compras = Compra.objects.all()
    form = CompraForm()
    return render(request, "compras/compras.html", {"compras": compras, "form": form})

def registrarCompra(request):
    compra = Compra.objects.create(producto_id = request.POST['producto'],
                                   cantidad = request.POST['cantidad'],
                                   total = request.POST['total']
                                   )
    producto = get_object_or_404(Producto, pk=request.POST['producto'])
    producto.stock_disponible += int(compra.cantidad)
    producto.save()
    return redirect('compras')

def verDetalleCompra(request, id):
    if request.method == 'GET':
        compra=get_object_or_404(Compra, pk=id)
        form = CompraForm(instance=compra)
        return render(request, 'compras/detalleCompra.html', {"compra": compra, "form": form})
    else:
        try:
            compra=get_object_or_404(Compra, pk=id)
            form = CompraForm(request.POST, instance=compra)
            if form.is_valid():
                compra.save()
                return redirect('compras')
        except ValueError:
            return render(request, 'compras',{
                'error': "error editando la compra"
            })


def eliminarCompra(request, id):
    compra = get_object_or_404(Compra, id=id)
    compra.delete()
    return redirect('compras')