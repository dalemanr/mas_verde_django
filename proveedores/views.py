from django.shortcuts import render, redirect
from compras.models import Proveedor
from .forms import ProveedorForm
from registration.views import group_required

@group_required("Administrador")
def item_list(request):
    items = Proveedor.objects.all()
    return render(request, 'proveedores/item_list.html', {'items': items})

@group_required("Administrador")
def item_detail(request, pk):
    item = Proveedor.objects.get(pk=pk)
    return render(request, 'proveedores/item_detail.html', {'item': item})

@group_required("Administrador")
def item_create(request):
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ProveedorForm()
    return render(request, 'proveedores/item_form.html', {'form': form})

@group_required("Administrador")
def item_update(request, pk):
    item = Proveedor.objects.get(pk=pk)
    if request.method == 'POST':
        form = ProveedorForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('item_list')
    else:
        form = ProveedorForm(instance=item)
    return render(request, 'proveedores/item_form.html', {'form': form})

@group_required("Administrador")
def item_delete(request, pk):
    item = Proveedor.objects.get(pk=pk)
    if request.method == 'POST':
        item.delete()
        return redirect('item_list')
    return render(request, 'proveedores/item_confirm_delete.html', {'item': item})
