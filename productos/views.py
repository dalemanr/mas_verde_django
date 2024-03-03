from django.shortcuts import render, redirect
from compras.models import Producto
from compras.models import Proveedor
from django.contrib import messages


###########CRUD PRODUCTOS##################

def index(request):
    productoListados= Producto.objects.all()
    messages.success(request, '¡Productos Listados!')
    return render(request, "gestionP.html", {"productos": productoListados})

def registrarProducto(request):
 if request.method == 'POST':
    nombre=request.POST['txtNombre']
    descripcion=request.POST['txtDescripcion']
    precio=request.POST['txtPrecio']
    stock_disponible=request.POST['txtStock_Disponible']
    fecha_creacion=request.POST['txtFecha_Creacion']
    proveedor=request.POST['txtProveedor']
    
    producto = Producto.objects.create(nombre=nombre,descripcion=descripcion,precio=precio,stock_disponible=stock_disponible,fecha_creacion=fecha_creacion,proveedor=proveedor)
    messages.success(request, '¡Producto Registrado!')
    return redirect('productos')
 else: 
     
     return render(request, 'gestionP.html')

def editarProducto(request, nombre):
    producto=Producto.objects.get(nombre=nombre)
    return render(request, "editarProducto.html", {"producto":producto})

def edicionProducto(request,id):
    if request.method == 'POST':
        nombre=request.POST['txtNombre']
        descripcion=request.POST['txtDescripcion']
        precio=request.POST['txtPrecio']
        stock_disponible=request.POST['txtStock_Disponible']
        fecha_creacion=request.POST['txtFecha_Creacion']
        proveedor=request.POST['txtProveedor']
        
        producto=Producto.objects.get(id=id)
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock_disponible = stock_disponible
        producto.fecha_creacion = fecha_creacion
        producto.proveedor = proveedor
        producto.save()
        messages.success(request, '¡Producto Editado!')
        return redirect('productos')

def eliminarProducto(request, id):
    producto=Producto.objects.get(id=id)
    producto.delete()
    messages.success(request, '¡Producto Eliminado!')
    return redirect('productos')