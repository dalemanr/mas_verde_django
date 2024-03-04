from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CompraForm

from compras.models import *
# Create your views here.

####################CRUD PRODUCTOS#######################












####################CRUD PROVEEDORES######################
















########################CRUD COMPRAS##########################

@login_required
def index(request):
    compras = Compra.objects.all()
    form = CompraForm()
    return render(request, "compras/compras.html", {"compras": compras, "form": form})

@login_required
def registrarCompra(request):
    compra = Compra.objects.create(producto_id = request.POST['producto'],
                                   cantidad = request.POST['cantidad'],
                                   total = request.POST['total']
                                   )
    producto = get_object_or_404(Producto, pk=request.POST['producto'])
    producto.stock_disponible += int(compra.cantidad)
    producto.save()
    return redirect('compras')

@login_required
def verDetalleCompra(request, id):
    if request.method == 'GET':
        compra=get_object_or_404(Compra, pk=id)
        form = CompraForm(instance=compra)
        return render(request, 'compras/detalleCompra.html', {"compra": compra, "form": form})
    else:
        try:
            comprainit=get_object_or_404(Compra, pk=id)
            compra=get_object_or_404(Compra, pk=id)
            producto = compra.producto
            cant1=comprainit.cantidad
            form = CompraForm(request.POST, instance=compra)
            if form.is_valid():
                compra.save()
                cant2= compra.cantidad
                cantidad=cant2-cant1

                if cant2>cant1:
                    producto.stock_disponible += int(cantidad)
                    producto.save()
                elif cant2<cant1:
                    producto.stock_disponible -= abs(cantidad)
                    producto.save()
                else:
                    pass

                return redirect('compras')
        except ValueError:
            return render(request, 'compras',{
                'error': "error editando la compra"
            })

@login_required
def eliminarCompra(request, id):
    compra = get_object_or_404(Compra, id=id)
    producto = compra.producto
    cantidad = compra.cantidad
    producto.stock_disponible -= int(cantidad)
    producto.save()
    compra.delete()
    return redirect('compras')