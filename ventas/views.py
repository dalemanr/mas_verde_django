from django.core.mail import EmailMessage

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.urls import reverse
from xhtml2pdf import pisa

from compras.models import Producto
from .models import Venta, DetalleVenta
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
        productos = Producto.objects.all()
    return render(request, 'ventas/registrar_venta.html',
                  {'venta_form': venta_form, 'detalle_venta_formset': detalle_venta_formset, 'productos': productos} )

@login_required
def recibo(request, venta_id):
    venta = Venta.objects.get(pk=venta_id)
    detalles_venta= venta.detalleventa_set.all()
    return render(request, 'ventas/recibo.html',{'venta':venta,'detalles_venta': detalles_venta})

def ventas_list(request):
    ventas = Venta.objects.all()
    return render(request, 'ventas/ventas_list.html', {
        'ventas': ventas
    })

@login_required
def productos_mas_vendidos(request):
    ventas = DetalleVenta.objects.values('producto__nombre').annotate(total_ventas=Sum('cantidad')).order_by('-total_ventas')

    template_path = 'ventas/productos_mas_vendidos.html'
    template = get_template(template_path)

    context = {'ventas': ventas}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Reporte_productos_mas_vendidos.pdf"'

    pisa_statuts = pisa.CreatePDF(
        html, dest=response
    )

    if pisa_statuts.err:
        return HttpResponse('Error al generar pdf', status=500)
    
    return response

@login_required
def generar_pdf(request, venta_id):
    venta = Venta.objects.get(pk=venta_id)
    detalles_venta= venta.detalleventa_set.all()

    template_path = 'ventas/generar_pdf.html'
    template = get_template(template_path)

    context = {'venta': venta, 'detalles_venta': detalles_venta}
    html = template.render(context)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="venta.pdf"'

    pisa_statuts = pisa.CreatePDF(
        html, dest=response
    )

    if pisa_statuts.err:
        return HttpResponse('Error al generar pdf', status=500)
    enviar_correo_con_pdf(response.content, 'venta.pdf', venta.cliente.correo)
    return response

@login_required
def enviar_correo_con_pdf(pdf_bytes, pdf_filename, destinatario):

    email = EmailMessage(
        subject='Recibo de compra en tienda FUNAT S.A.S',
        body='Adjunto encontrarás tu recibo de compra.',
        from_email='jose.aleman7@misena.edu.co',
        to=[destinatario],
    )

    #Ejemplos de para agregar elementos de una lista a otra lista ya existente

    #lista_de_correos = []

    # email.to.append(element for element in lista_de_correos)
    # email.to.extend(lista_de_correos)
    # email.to + lista_de_correos

    email.attach(filename=pdf_filename, content=pdf_bytes, mimetype='application/pdf')

    email.send()

