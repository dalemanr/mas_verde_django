import locale
from calendar import month_name
from datetime import datetime

from django.shortcuts import render, redirect

from perdidas.forms import PerdidaForm
from perdidas.models import Perdida
from registration.views import group_required


# Create your views here.
@group_required("Administrador")


def index(request):
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
    now = datetime.now()

    mes_actual = datetime.now().month
    año_actual = datetime.now().year

    numero_mes = int(datetime.now().month)
    nombre_mes = month_name[numero_mes]


    perdidas_por_mes = Perdida.objects.filter(fecha_perdida__month=mes_actual, fecha_perdida__year=año_actual)

    form = PerdidaForm()
    return render(request, "perdidas/perdidas.html", {"perdidas": perdidas_por_mes, "form": form, 'fecha': now, 'mes': nombre_mes})

def registroPerdida(request):
    if request.method == 'POST':
        producto = (request.POST["producto"])
        cantidad = int(request.POST["cantidad"])
        causa = (request.POST["causa"])

        perdida = Perdida(producto_id=producto, cantidad=cantidad, causa=causa)
        producto = perdida.producto
        producto.stock_disponible -= cantidad
        producto.save()
        perdida.save()
        return redirect('perdidas')