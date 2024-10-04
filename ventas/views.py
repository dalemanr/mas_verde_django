import locale

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
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from datetime import datetime, timedelta
from calendar import month_name

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

    # Número de elementos por página
    elementos_por_pagina = 5
    paginator = Paginator(ventas, elementos_por_pagina)

    # Obtener el número de página solicitado (si hay)
    pagina = request.GET.get('page')

    try:
        # Obtener los objetos de la página solicitada
        ventas_paginadas = paginator.page(pagina)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        ventas_paginadas = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango, mostrar la última página
        ventas_paginadas = paginator.page(paginator.num_pages)

    return render(request, 'ventas/ventas_list.html', {
        'ventas': ventas_paginadas
    })


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
        return HttpResponse('Error al generar pdfss', status=500)
    enviar_correo_con_pdf(response.content, 'venta.pdf', venta.cliente.correo)
    return response


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


def ganancias_producto(request):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    now = datetime.now()
    mes_actual = now.month
    año_actual = now.year

    numero_mes = int(now.month)
    nombre_mes = month_name[numero_mes]


    primer_dia_mes_actual = datetime(año_actual, mes_actual, 1)
    ultimo_dia_mes_actual = datetime(año_actual, mes_actual, 1).replace(day=28)
    ultimo_dia_mes_actual = ultimo_dia_mes_actual + timedelta(days=(4 - ultimo_dia_mes_actual.weekday()))

    productos = Producto.objects.all()
    ganancias_por_producto = {}

    for producto in productos:
        detalles_venta = DetalleVenta.objects.filter(producto=producto, venta__fecha__range=[primer_dia_mes_actual, ultimo_dia_mes_actual])
        ganancia_producto = detalles_venta.aggregate(total_ganancia=Sum('subtotal'))['total_ganancia'] or 0

        ganancias_por_producto[producto.nombre] = ganancia_producto

    return render(request, 'ventas/ganancias_producto.html', {'productos': productos, 'ganancias_por_producto': ganancias_por_producto , 'fecha': now, 'mes': nombre_mes})

@login_required
def productos_mas_vendidos(request):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    now = datetime.now()
    mes_actual = datetime.now().month
    año_actual = datetime.now().year

    numero_mes = int(now.month)
    nombre_mes = month_name[numero_mes]

    # Filtrar las ventas por el mes actual
    ventas_por_mes = DetalleVenta.objects.filter(venta__fecha__month=mes_actual, venta__fecha__year=año_actual) \
                                         .values('producto__nombre') \
                                         .annotate(total_ventas=Sum('cantidad')) \
                                         .order_by('-total_ventas')

    return render(request, 'ventas/productos_mas_vendidos.html', {'ventas': ventas_por_mes, 'fecha': now, 'mes': nombre_mes})
