from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Clientes
from django.contrib import messages
from registration.views import group_required
from django.contrib.auth.decorators import login_required
###########CRUD CLIENTES####################

@login_required
def index(request):
    if group_required('Vendedor'):
        clientelistado = Clientes.objects.all()
        messages.success(request, '¡Clientes Listados!')
        return render(request, "gestionC.html", {"clientes": clientelistado})
    else:
        return HttpResponseRedirect('Mal ahí, no tenes permiso de acceder aqui raton')

@login_required
def registrarCliente(request):
 if request.method == 'POST':
    nombre=request.POST['txtNombre']
    apellido=request.POST['txtApellido']
    documento=request.POST['txtDocumento']
    telefono=request.POST['txtTelefono']
    correo=request.POST['txtCorreo']
    
    
    clientes = Clientes.objects.create(nombre=nombre,apellido=apellido,documento=documento,telefono=telefono,correo=correo)
    messages.success(request, '¡Cliente Registrado!')
    return redirect(request.META.get('HTTP_REFERER', '/'))
 else: 
     
     return render(request, 'gestionC.html')

@login_required
def editarClientes(request,id):
    clientes=Clientes.objects.get(id=id)
    return render(request, "editarClientes.html" , {"clientes":clientes})

@login_required
def edicionClientes(request,id):
    if request.method == 'POST':
        nombre = request.POST.get('txtNombre')
        apellido = request.POST.get('txtApellido')
        documento = request.POST.get('txtDocumento')
        telefono = request.POST.get('txtTelefono')
        correo = request.POST.get('txtCorreo')
    
        clientes=Clientes.objects.get(id=id)
        clientes.apellido = apellido
        clientes.documento = documento
        clientes.telefono = telefono
        clientes.correo = correo
        clientes.save()
        messages.success(request, '¡Cliente Editado!')
        return redirect('clientes')

@login_required
def eliminarClientes(request, id):
    clientes=Clientes.objects.get(id=id)
    clientes.delete()
    messages.success(request, '¡Cliente Eliminado!')
    return redirect('clientes')