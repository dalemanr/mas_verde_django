from django.shortcuts import render, redirect
from django.core.mail import EmailMessage
from .forms import FormularioContacto
from pqrs.models import Pqrs
import datetime as dt

def index(request):
    return render(request, 'emails/email.html')

def correo(request,id):
    cliente=Pqrs.objects.get(id=id)
    formulario_contacto = FormularioContacto()

    if request.method == "POST":
        formulario_contacto = FormularioContacto(data=request.POST)
        if formulario_contacto.is_valid():
            cliente.estado = "Respondido"
            cliente.fecha_respuesta = dt.datetime.now()
            cliente.save()
            nombre = cliente.nombre
            email = cliente.correo
            asunto = request.POST.get("asunto")
            contenido = request.POST.get("contenido")

            email = EmailMessage(
                asunto,
                "El usuario con nombre {}  de parte de Funat S.A.S ha escrito lo siguiente:\n\n{}".format(nombre, contenido),
                '',
                [email],  
                reply_to=[email]
            )

            try:
                email.send()
                return redirect("/pqrs/listado_pqrs")
            except:
                return redirect("/send_email/?novalido")

    return render(request, "emails/email.html", {'miFormulario': formulario_contacto, 'pqrs':cliente})
