from django.shortcuts import render, redirect
from compras.models import Producto
from compras.models import Proveedor
from django.contrib import messages
from compras.forms import ImagenForm
from registration.views import group_required

###########CRUD PRODUCTOS##################
def index(request):
    productoListados= Producto.objects.all()
    proveedores= Proveedor.objects.all()
    messages.success(request, '¡Productos Listados!')
    return render(request, "gestionP.html", {"productos": productoListados,
                                             "proveedores": proveedores,})
@group_required("Administrador")
def registrarProducto(request):
 form = ImagenForm
 if request.method == 'POST':
    nombre=request.POST['txtNombre']
    descripcion=request.POST['txtDescripcion']
    stock_disponible=request.POST['txtStock_Disponible']
    proveedor=request.POST['txtProveedor']
    imagen=request.FILES['imagen']
    producto = Producto.objects.create(nombre=nombre,descripcion=descripcion,stock_disponible=stock_disponible,proveedor_id=proveedor, imagen=imagen)
    messages.success(request, '¡Producto Registrado!')
    return redirect('productos')
 else: 

     return render(request, 'gestionP.html',{'form': form})

@group_required("Administrador")
def editarProducto(request, id):
    producto=Producto.objects.get(id=id)
    proveedores= Proveedor.objects.all()
    return render(request, "editarProducto.html", {"producto":producto,
                                                   "proveedores": proveedores})

@group_required("Administrador")
def edicionProducto(request,id):
    if request.method == 'POST':
        nombre=request.POST['txtNombre']
        descripcion=request.POST['txtDescripcion']
        precio=request.POST['txtPrecio']
        stock_disponible=request.POST['txtStock_Disponible']

        proveedor=request.POST['txtProveedor']
        
        producto=Producto.objects.get(id=id)
        producto.descripcion = descripcion
        producto.precio = precio
        producto.stock_disponible = stock_disponible

        producto.proveedor_id = proveedor
        producto.save()
        messages.success(request, '¡Producto Editado!')
        return redirect('productos')

@group_required("Administrador")
def eliminarProducto(request, id):
    producto=Producto.objects.get(id=id)
    producto.delete()
    messages.success(request, '¡Producto Eliminado!')
    return redirect('productos')