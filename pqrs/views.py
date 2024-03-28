from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pqrs 

# Create your views here.

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def index(request):
    pqrs = Pqrs.objects.all()

    # Número de elementos por página
    elementos_por_pagina = 1
    paginator = Paginator(pqrs, elementos_por_pagina)

    # Obtener el número de página solicitado (si hay)
    pagina = request.GET.get('page')

    try:
        # Obtener los objetos de la página solicitada
        pqrs_paginadas = paginator.page(pagina)
    except PageNotAnInteger:
        # Si la página no es un número entero, mostrar la primera página
        pqrs_paginadas = paginator.page(1)
    except EmptyPage:
        # Si la página está fuera del rango, mostrar la última página
        pqrs_paginadas = paginator.page(paginator.num_pages)

    return render(request, 'pqrs/registro_pqrs.html', {
        'pqrs': pqrs_paginadas
    })


def registrarPqrs(request):
    if request.method == 'POST':
        fecha=request.POST.get('txtFecha')
        asunto=request.POST.get('txtAsunto')
        detalle=request.POST.get('txtDetalle')
        nombre=request.POST.get('txtNombre')
        apellido=request.POST.get('txtApellido')
        correo=request.POST.get('txtCorreo')
        
        pqrs=Pqrs(
            fecha=fecha,
            asunto=asunto,
            detalle=detalle,
            nombre=nombre,
            apellido=apellido,
            correo=correo
        )
        
        pqrs.save()
        messages.success(request, '¡Tu solicitud esta siendo procesada!')
        return redirect('inicio')


def listar_pqrs(request):
    pqrs=Pqrs.objects.all()

    data={
        "pqrs":pqrs
    }
    return render(request, 'pqrs/listado_pqrs.html',data)


def eliminarPqrs(request, id):
    pqrs=Pqrs.objects.get(id=id)
    pqrs.delete()
    messages.success(request, '¡Pqrs Eliminada!')
    return redirect('inicio')


