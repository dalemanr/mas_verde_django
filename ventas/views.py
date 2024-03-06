from django.shortcuts import render, redirect
from .models import Venta, DetalleVenta
from .forms import VentaForm, DetalleVentaFormSet

def registrar_venta(request):
    if request.method == 'POST':
        venta_form = VentaForm(request.POST)
        detalle_venta_formset = DetalleVentaFormSet(request.POST)
        if venta_form.is_valid() and detalle_venta_formset.is_valid():
            venta = venta_form.save()
            for detalle_venta_form in detalle_venta_formset:
                detalle_venta = detalle_venta_form.save(commit=False)
                detalle_venta.venta = venta
                detalle_venta.save()
            return redirect('ventas:lista_ventas')  # Redireccionar a la página de lista de ventas o a donde desees
    else:
        venta_form = VentaForm()
        detalle_venta_formset = DetalleVentaFormSet()
    return render(request, 'ventas/registrar_venta.html', {'venta_form': venta_form, 'detalle_venta_formset': detalle_venta_formset})
