from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Venta
from .forms import VentaForm, DetalleVentaFormSet

@login_required
def registrar_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_venta_formset = DetalleVentaFormSet(request.POST)
        if venta_form.is_valid() and detalle_venta_formset.is_valid():
            for detalle_venta_form in detalle_venta_formset:
                detalle_venta = detalle_venta_form.save(commit=False)
                detalle_venta.subtotal = detalle_venta.producto.precio * detalle_venta.cantidad

                if detalle_venta.cantidad > detalle_venta.producto.stock_disponible:
                    return HttpResponse('Lo sentimos, no contamos con tal cantidad de productos para venderle :(')

            venta = venta_form.save(commit=False)
            venta.vendedor = request.user
            venta.save()

            for detalle_venta_form in detalle_venta_formset:
                detalle_venta = detalle_venta_form.save(commit=False)
                detalle_venta.venta = venta
                detalle_venta.producto.stock_disponible -= detalle_venta.cantidad
                venta.total += detalle_venta.subtotal
                venta.save()
                detalle_venta.save()
                detalle_venta.producto.save()

            return redirect(reverse('recibo', kwargs={'venta_id': venta.pk}))
    else:
        venta_form = VentaForm()
        detalle_venta_formset = DetalleVentaFormSet()
    return render(request, 'ventas/registrar_venta.html',
                  {'venta_form': venta_form, 'detalle_venta_formset': detalle_venta_formset})

@login_required
def recibo(request, venta_id):
    venta = Venta.objects.get(pk=venta_id)
    detalles_venta= venta.detalleventa_set.all()
    return render(request, 'ventas/recibo.html',{'venta':venta,'detalles_venta': detalles_venta})