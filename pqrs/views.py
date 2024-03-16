from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Pqrs 

# Create your views here.

def index(request):
    pqrs=Pqrs.objects.all()
    data = {
        "pqrs":pqrs,
    }
    return render(request,'pqrs/registro_pqrs.html',data)

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


