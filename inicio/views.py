from django.shortcuts import render
from compras.models import Producto
# Create your views here.
def index(request):
    productos = Producto.objects.all()
    return render(request, "home.html", {"productos": productos})