from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from compras.models import *
from registration.views import group_required
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
# Create your views here.

####################CRUD Compras#######################

@group_required("Administrador")
def index(request):
    compras = Compra.objects.all()
    form = CompraForm()
    return render(request, "compras/compras.html", {"compras": compras, "form": form})


@group_required("Administrador")
def registrarCompra(request):
    total = int(request.POST["total"])
    cantidad = int(request.POST["cantidad"])
    porcentaje_ganancia = int(request.POST["porcentaje_ganancia"])
    precio_unitario = total/cantidad
    compra = Compra.objects.create(producto_id = request.POST['producto'],
                                   cantidad = request.POST['cantidad'],
                                   total = request.POST['total'],
                                   precio_unitario = precio_unitario,
                                   porcentaje_ganancia = porcentaje_ganancia)
    producto = get_object_or_404(Producto, pk=request.POST['producto'])
    producto.stock_disponible += int(compra.cantidad)
    producto.precio = compra.precio_unitario+(compra.precio_unitario*(porcentaje_ganancia/100))
    producto.save()
    return redirect('compras')


@group_required("Administrador")
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

                compra = form.save(commit=False)
                compra.precio_unitario = compra.total/compra.cantidad
                cant2= compra.cantidad
                cantidad=cant2-cant1

                if cant2>cant1:
                    producto.stock_disponible += int(cantidad)
                    producto.precio = round(compra.precio_unitario + (compra.precio_unitario * (compra.porcentaje_ganancia / 100)))
                    producto.save()
                elif cant2<cant1:
                    producto.stock_disponible -= abs(cantidad)
                    producto.precio = round(compra.precio_unitario + (compra.precio_unitario * (compra.porcentaje_ganancia / 100)))
                    producto.save()
                else:
                    producto.precio = round(compra.precio_unitario + (compra.precio_unitario * (compra.porcentaje_ganancia / 100)))
                    producto.save()
                compra.save()

                return redirect('compras')
        except ValueError:
            return render(request, 'compras',{
                'error': "error editando la compra"
            })


@group_required("Administrador")
def eliminarCompra(request, id):
    compra = get_object_or_404(Compra, id=id)
    producto = compra.producto
    cantidad = compra.cantidad
    producto.stock_disponible -= int(cantidad)
    producto.save()
    compra.delete()
    return redirect('compras')

def compras_por_proveedor(request):
    proveedores = Proveedor.objects.all()
    compras_por_proveedor = {}
    for proveedor in proveedores:
        compras = Compra.objects.filter(producto__proveedor=proveedor)
        compras_por_proveedor[proveedor.nombre] = compras

    template_path = 'compras/productos.html'
    template = get_template(template_path)

    context = {'compras_por_proveedor': compras_por_proveedor}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte_compras_a_proveedores.pdf"'

    pisa_statuts = pisa.CreatePDF(
        html, dest=response
    )

    if pisa_statuts.err:
        return HttpResponse('Error al generar pdf', status=500)
    
    return response