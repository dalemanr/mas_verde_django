from django.shortcuts import render

# Create your views here.

####################CRUD PRODUCTOS#######################












####################CRUD PROVEEDORES######################
















########################CRUD COMPRAS##########################

def compras(request):
    return render(request, "compras/compras.html")