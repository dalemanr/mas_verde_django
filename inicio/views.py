from django.shortcuts import render
from compras.models import Producto
# Create your views here.
def index(request):
    productos = Producto.objects.all()
    user = request.user
    return render(request, "home.html", {"productos": productos, "user": user})

